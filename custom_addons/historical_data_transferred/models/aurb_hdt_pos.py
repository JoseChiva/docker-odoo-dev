from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPos(models.Model):
    _name = "aurb.hdt.pos"
    _description = "AURB POS"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    tpv = fields.Integer()
    titulo = fields.Char()
    tras_contab = fields.Integer()
    tras_ticket = fields.Integer()
    tras_cobros = fields.Integer()
    agrupar = fields.Integer()
    impresora_1 = fields.Char()
    impresora_2 = fields.Char()
    impresora_3 = fields.Char()
    impresora_4 = fields.Char()
    moneda = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.tpv != False:
                view_name += ' ' + str(record.tpv)
            record.display_name = view_name