from odoo import models, fields


class Tag(models.Model):
    _name = "task.tag"
    _description = "Tag"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(default=0)
    task_ids = fields.Many2many(
        "task.task",
        relation="task_task_tag_rel",
        column1="tag_id",
        column2="task_id",
        string="Tasks",
    )
