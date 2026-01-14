from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtDefaultPrinter(models.Model):
    _name = "aurb.hdt.default.printer"
    _description = "AURB Default printer"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    usuario = fields.Char()
    tipo_doc = fields.Char()
    impresora = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.usuario != False:
                view_name += ' ' + record.usuario
            if record.impresora != False:
                view_name += ' ' + record.impresora
            record.display_name = view_name