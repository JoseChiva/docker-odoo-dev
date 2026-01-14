from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCountry(models.Model):
    _name = "aurb.hdt.country"
    _description = "AURB Country"
    _rec_name = "name"
    _order = "name desc"

    name = fields.Char(index=True, required=True)
    pais = fields.Char()
    nombre = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.nombre != False:
                view_name = record.nombre
            record.display_name = view_name
