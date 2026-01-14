from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtKeys(models.Model):
    _name = "aurb.hdt.keys"
    _description = "AURB Keys"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    codigo_id = fields.Many2one("aurb.hdt.items")
    clave = fields.Char()
    descripcion = fields.Char()
    valor = fields.Char()
    tipo = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.clave != False:
                view_name += ' ' + record.clave
            record.display_name = view_name