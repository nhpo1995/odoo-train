import logging
import re
from datetime import datetime, timedelta
from typing import Optional

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _name = "task.task"
    _description = "Task"

    name = fields.Char(string="Task Name", required=True, copy=False)
    description = fields.Text(string="Task Description", required=True)

    @api.model
    def _expand_states(self, states, domain, order):
        return ["draft", "in_progress", "done"]

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        default="draft",
        required=True,
        group_expand="_expand_states",
    )
    priority = fields.Selection(
        string="Priority",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )

    due_date = fields.Datetime(string="Due Date", help="Task deadline")
    hours_estimated = fields.Float(string="Estimated Hours", digits=(6, 2))
    hours_spent = fields.Float(string="Hour Spent", digits=(6, 2))
    is_overdue = fields.Boolean(
        string="The task is overdue",
        readonly=True,
        compute="_compute_is_overdue",
        search="_search_is_overdue",
        # store = False by default!
    )
    color = fields.Integer(string="color in integer", store=True)

    project_id = fields.Many2one(
        comodel_name="task.project",
        string="Project",
        ondelete="cascade",
        index=True,
    )
    assigned_user_id = fields.Many2one(
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "task.tag",
        relation="task_task_tag_rel",
        column1="task_id",
        column2="tag_id",
        string="Tags",
    )
    has_urgent_tags = fields.Boolean(
        string="Has Urgent tag",
        compute="_compute_has_urgent_tag",
        store=False,
    )

    hours_remaining = fields.Float(
        digits=(6, 2),
        compute="_compute_hours_remaining",
        store=True,
    )

    progress = fields.Float(
        store=True,
        compute="_compute_progress",
        inverse="_inverse_progress",
    )

    _sql_constraints = [
        (
            "name_project_id_unique",
            "UNIQUE(project_id, name)",
            _("Task title must be unique within the same Project!"),
        ),
        (
            "hours_estimated_check",
            "CHECK(hours_estimated >= 0)",
            _("Hours estimated should be greater or equal to 0!"),
        ),
        (
            "hours_spent_check",
            "CHECK(hours_spent >= 0)",
            _("Hours spent should be greater or equal to 0!"),
        ),
    ]

    @api.constrains("hours_spent", "hours_estimated", "state")
    def _check_hours_on_done(self):
        for rec in self:
            if (
                rec.state == "done"
                and float_compare(rec.hours_spent, rec.hours_estimated, 2) > 0
            ):
                raise ValidationError(
                    _(
                        "Hours spent should not exceed the estimated hours for a Done task."
                    )
                )

    @api.constrains("due_date")
    def _check_due_date(self):
        now: datetime = fields.Datetime.now()
        for rec in self:
            if rec.due_date and rec.due_date < now:
                raise ValidationError(
                    _("Due date should be greater than the present datetime!")
                )

    @api.depends("hours_spent", "hours_estimated", "state")
    def _compute_progress(self):
        for rec in self:
            if rec.hours_estimated <= 0:
                rec.progress = 0
            else:
                rec.progress = (rec.hours_spent / rec.hours_estimated) * 100
            if rec.state == "done":
                rec.progress = 100

    def _inverse_progress(self):
        for rec in self:
            if rec.state == "done":
                rec.hours_estimated = rec.hours_spent
            else:
                rec.hours_spent = (rec.progress / 100) * rec.hours_estimated

    @api.depends("hours_estimated", "hours_spent")
    def _compute_hours_remaining(self):
        for rec in self:
            rec.hours_remaining = rec.hours_estimated - rec.hours_spent

    def _search_is_overdue(self, operator, value):
        now = fields.Datetime.now()
        if operator == "=" and value is True:
            return [("due_date", "<", now), ("state", "!=", "done")]
        elif operator == "=" and value is False:
            return ["|", ("due_date", ">=", now), ("state", "=", "done")]
        return []

    @api.depends("tag_ids", "tag_ids.name")
    def _compute_has_urgent_tag(self):
        for rec in self:
            if rec.tag_ids and hasattr(rec.tag_ids, "mapped"):
                rec.has_urgent_tags = "urgent" in rec.tag_ids.mapped("name")
            else:
                rec.has_urgent_tags = False

    @api.depends("due_date", "state")
    def _compute_is_overdue(self):
        now: datetime = fields.Datetime.now()
        for rec in self:
            due: Optional[datetime] = fields.Datetime.to_datetime(rec.due_date)
            rec.is_overdue = bool(due and due < now and rec.state != "done")

    @api.model_create_multi
    def create(self, vals_list):
        """Override"""
        for vals in vals_list:
            _logger.info(f"Create task with vals: {vals}")
        records = super().create(vals_list)
        _logger.info(f"Created task with ids: {records.ids}")
        return records

    def write(self, vals):
        """Override"""
        if "state" in vals:
            for record in self:
                _logger.info(
                    f"Task {record.id}: state changing from {record.state} to {vals['state']}"  # type: ignore
                )

        for record in self:
            is_done = vals.get("state") == "done" or record.state == "done"
            if is_done:
                priority = vals.get("priority", record.priority)
                if not priority:
                    raise UserError("Cannot remove priority from done task!")
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == "done":
                raise UserError("Cannot delete a done task!")
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        if "name" not in default:
            name = self.name
            if name:
                match = re.search(r" \(copy( \d+)?\)$", name)
                if match:
                    name = name[: match.start()]
                new_name = f"{name} (copy)"
                copy_count = 1
                while (
                    self.search_count(
                        [
                            ("name", "=", new_name),
                            ("project_id", "=", self.project_id.id),  # type: ignore
                        ]
                    )
                    > 0
                ):
                    new_name = f"{name} (copy {copy_count})"
                    copy_count += 1
                default["name"] = new_name
        return super().copy(default)

    def action_mark_done(self):
        """Mark tasks as done."""
        self.write({"state": "done"})

    def action_delete(self):
        """Delete selected tasks."""
        _logger.info(f"Deleting tasks: {self.ids}")
        self.unlink()
        _logger.info("Delete completed")

    def action_admin_only(self):
        _logger.info("Action Admin!")
        pass

    def action_mark_urgent(self):
        """Button: Add urgent tag to task"""
        urgent_tag = self.env["task.tag"].search([("name", "=", "urgent")], limit=1)  # type: ignore
        if not urgent_tag:
            urgent_tag = self.env["task.tag"].create({"name": "urgent", "color": 1})  # type: ignore
        self.write({"tag_ids": [(4, urgent_tag.id, 0)]})

    def action_remove_all_tags(self):
        self.write({"tag_ids": [(5, 0, 0)]})

    def action_clean_draft(self):
        # 1. Tìm batch (tối ưu query)
        time_limit = fields.Datetime.now() - timedelta(days=7)
        draft_tasks = self.search(
            [
                ("state", "=", "draft"),
                ("create_date", "<", time_limit),
            ]
        )
        # 2. Xóa batch (1 lệnh DELETE duy nhất cho N records)
        draft_tasks.unlink()
        # 3. Return action reload (Client Action)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": f"Deleted {len(draft_tasks)} tasks successfully!",
                "type": "success",
                "sticky": False,
                "next": {"type": "ir.actions.client", "tag": "reload"},
            },
        }

    @api.onchange("project_id")
    def _onchange_project_id(self):
        for rec in self:
            if rec.project_id:
                if rec.project_id.manager_id:
                    rec.assigned_user_id = rec.project_id.manager_id
                else:
                    return {
                        "warning": {
                            "title": _("Warning"),
                            "message": _("This project has no manager assigned!"),
                        }
                    }
