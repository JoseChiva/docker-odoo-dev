from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtItemsDesc(models.Model):
    _name = "aurb.hdt.items.desc"
    _description = "AURB Items Desc"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    codigo_id = fields.Many2one("aurb.hdt.items")
    clv_art = fields.Integer()

    tipo = fields.Integer()
    subcta = fields.Char()
    idioma = fields.Integer()
    descripcion = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.descripcion != False:
                view_name += ' ' + record.descripcion
            record.display_name = view_name