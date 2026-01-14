from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtSubaccounts(models.Model):
    _name = "aurb.hdt.subaccounts"
    _description = "AURB Subaccounts"
    _rec_name = "name"

    name = fields.Char()
    empresa = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company",string = "Empresa nombre")
    subcta = fields.Char()
    titulo = fields.Char()
    manual = fields.Char()
    ficha_cerrada = fields.Char()
    pedir_centro = fields.Char()
    obligatorio = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta != False:
                view_name += ' ' + record.subcta
            record.display_name = view_name