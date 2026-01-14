from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCompUserParameters(models.Model):
    _name = "aurb.hdt.compuser.parameters"
    _description = "AURB Parameters per company/user"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    usuario = fields.Char()
    codigo = fields.Integer()
    descripcion_1 = fields.Char()
    descripcion_2 = fields.Char()
    v_int = fields.Integer()
    v_dec1 = fields.Float()
    v_dec2 = fields.Float()
    v_char = fields.Char()
    parametro = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.usuario != False:
                view_name += ' ' + record.usuario
            if record.codigo != False:
                view_name += ' ' + record.codigo
            record.display_name = view_name