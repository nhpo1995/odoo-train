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
