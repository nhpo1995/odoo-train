import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"
    _rec_name = "name"

    name = fields.Char(required=True, index=True)
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one("library.book", string="Parent Book")

    def name_get(self):
        _logger.info("name_get called with ids=%s len=%s", self.ids, len(self))
        return [(rec.id, f"[{rec.id}] {rec.name}") for rec in self]  # type: ignore
