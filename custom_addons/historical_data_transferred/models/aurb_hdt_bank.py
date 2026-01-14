from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtBank(models.Model):
    _name = "aurb.hdt.bank"
    _description = "AURB Bank"
    _rec_name = "name"
    _order = "nif desc"

    name = fields.Char(index=True, required=True)
    empresa = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company",string = 'empresa_id')
    subcta = fields.Char()
    nif = fields.Char()
    direccion = fields.Char()
    poblacion = fields.Char()
    pais = fields.Integer()
    provincia = fields.Integer()
    codigo_postal = fields.Integer()
    telefonos = fields.Char()
    numero_cta = fields.Char()
    limite_riesgo = fields.Float()
    observaciones = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if str(record.subcta) != False:
                view_name += ' ' + str(record.subcta)
            if record.nif != False:
                view_name += ' ' + str(record.nif)
            record.display_name = view_name
