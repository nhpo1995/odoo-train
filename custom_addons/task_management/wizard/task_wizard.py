from odoo import api, fields, models, _


class TaskWizard(models.TransientModel):
    _name = "task.wizard"
    _description = "Task Mass Update Wizard"

    new_state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="New State",
        required=True,
        default="draft",
    )

    def action_apply(self):
        # Get active_ids from context (passed by list view selection)
        active_ids = self.env.context.get("active_ids", [])
        if not active_ids:
            return

        # Use browse() to get recordset, then write()
        tasks = self.env["task.task"].browse(active_ids)
        tasks.write({"state": self.new_state})

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": _("Updated %s tasks successfully!") % len(tasks),
                "type": "success",
                "sticky": False,
                "next": {"type": "ir.actions.client", "tag": "reload"},
            },
        }
