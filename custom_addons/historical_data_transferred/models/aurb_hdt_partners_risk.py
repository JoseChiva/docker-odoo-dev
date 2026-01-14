from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersRisk(models.Model):
    _name = "aurb.hdt.partners.risk"
    _description = "AURB Partners Risk"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.partners")
    linea_producto = fields.Integer()
    clv_sub = fields.Integer()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    limite_credito = fields.Float()
    riesgo_cartera = fields.Float()
    riesgo_pedidos = fields.Float()
    fecha_u_compra = fields.Date()
    pts_no_factura = fields.Float()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            if record.moneda_id.moneda != False:
                view_name += ' ' + record.moneda_id.moneda
            record.display_name = view_name