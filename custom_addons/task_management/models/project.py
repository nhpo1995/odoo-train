from odoo import api, models, fields


class Project(models.Model):
    _name = "task.project"
    _description = "A project have many tasks"
    _rec_name = "name"

    name = fields.Char(string="Project Name", required=True, index=True)
    description = fields.Text()
    image = fields.Image(string="Cover", max_width=1920, max_height=1080)

    task_ids = fields.One2many(
        comodel_name="task.task", inverse_name="project_id", string="Tasks"
    )

    manager_id = fields.Many2one(
        comodel_name="res.users",
        string="Manager",
        default=lambda self: self.env.user,
    )

    task_count = fields.Integer(compute="_compute_task_count", store=True)

    @api.depends("task_ids")
    def _compute_task_count(self):
        for project in self:
            project.task_count = len(project.task_ids)

    total_revenue = fields.Float(
        string="Total Revenue", compute="_compute_statistics", store=False
    )
    total_hours = fields.Float(
        string="Total Hours", compute="_compute_statistics", store=False
    )

    @api.depends("task_ids.amount", "task_ids.hours_estimated")
    def _compute_statistics(self):
        # Optimization: Use read_group to calculate both sum in one query
        groups = self.env["task.task"].read_group(
            domain=[("project_id", "in", self.ids)],
            fields=["project_id", "amount:sum", "hours_estimated:sum"],
            groupby=["project_id"],
        )
        data_map = {
            g["project_id"][0]: {"amount": g["amount"], "hours": g["hours_estimated"]}
            for g in groups
            if g["project_id"]
        }

        for rec in self:
            stat = data_map.get(rec.id, {"amount": 0.0, "hours": 0.0})
            rec.total_revenue = stat["amount"]
            rec.total_hours = stat["hours"]
