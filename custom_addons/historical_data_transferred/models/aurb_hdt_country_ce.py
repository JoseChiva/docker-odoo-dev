from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCountryCe(models.Model):
    _name = "aurb.hdt.country.ce"
    _description = "AURB Country Ce"
    _rec_name = "name"
    _order = "name desc"

    name = fields.Char(index=True, required=True)
    pais_id = fields.Many2one("aurb.hdt.country")
    ce = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.pais_id.nombre != False:
                view_name = record.pais_id.nombre
            if record.ce != False:
                view_name += ' ' + record.ce
            record.display_name = view_name