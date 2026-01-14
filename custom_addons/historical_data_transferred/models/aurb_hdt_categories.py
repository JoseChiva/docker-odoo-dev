from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCategories(models.Model):
    _name = "aurb.hdt.categories"
    _description = "AURB Categories"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    categoria = fields.Integer()
    nombre = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.nombre
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo + ' ' + str(record.nombre)
            record.display_name = view_name