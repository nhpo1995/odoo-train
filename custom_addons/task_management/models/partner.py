from odoo import fields, models, api


class Partner(models.Model):
    _inherit = "res.partner"

    task_ids = fields.One2many(comodel_name="task.task", inverse_name="partner_id")

    task_count = fields.Integer(compute="_compute_task_count")

    @api.depends("task_ids")
    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)
