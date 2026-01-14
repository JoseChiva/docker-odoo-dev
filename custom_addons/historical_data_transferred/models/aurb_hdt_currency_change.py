from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCurrencyChange(models.Model):
    _name = "aurb.hdt.currency.change"
    _description = "AURB Currency Change"
    _rec_name = "name"
    _order = "name desc"

    name = fields.Char(index=True, required=True)
    moneda = fields.Char()
    moneda_ref = fields.Char()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    fecha_inicio = fields.Date()
    valor_c = fields.Float()
    valor_v = fields.Float()
    tipo = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.moneda_id.descripcion != False:
                view_name = record.moneda_id.descripcion
            if record.fecha_inicio != False:
                view_name += ' ' + str(record.fecha_inicio)
            record.display_name = view_name