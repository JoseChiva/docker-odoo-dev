from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtSellerCommission(models.Model):
    _name = "aurb.hdt.seller.commission"
    _description = "AURB Seller commission"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.seller")

    linea_producto = fields.Integer()
    clv_sub = fields.Integer()
    codigo = fields.Char()
    clv_art = fields.Integer()
    comision = fields.Float()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            if record.codigo != False:
                view_name += ' ' + record.codigo
            record.display_name = view_name