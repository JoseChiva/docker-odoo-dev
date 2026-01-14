from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtSellerCumulative(models.Model):
    _name = "aurb.hdt.seller.cumulative"
    _description = "AURB Seller cumulative"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.seller")

    linea_producto = fields.Integer()
    mes = fields.Integer()
    an = fields.Integer()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    pts_factura = fields.Float()
    pts_comis = fields.Float()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            if record.linea_producto != False:
                view_name += ' ' + record.linea_producto
            record.display_name = view_name