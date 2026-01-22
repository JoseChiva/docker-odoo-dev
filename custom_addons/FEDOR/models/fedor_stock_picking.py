
from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class FedorStockPicking(models.Model):
    _inherit = "stock.picking"

    fedor_product_packaging_qty = fields.Float(
        'Cantidad paquetes', compute='_compute_fedor_recalculate_packaging_qty')
    fedor_product_man_packaging_qty = fields.Float(
        'Cantidad paquetes manual')

    @api.depends('move_ids')
    def _compute_fedor_recalculate_packaging_qty(self):
        for head in self:
            qty = 0
            for line in head.move_ids:
                qty += line.fedor_product_packaging_qty
            head.fedor_product_packaging_qty = qty
