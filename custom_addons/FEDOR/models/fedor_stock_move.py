from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _

import math

import logging
_logger = logging.getLogger(__name__)


class FedorStockMove(models.Model):
    _inherit = "stock.move"

    fedor_product_packaging_qty = fields.Float(
        'Cantidad paquetes')
    fedor_location_id = fields.Many2one(
        'stock.location', string='Ubicación', compute="_getlocationline")
    fedor_location_store_id = fields.Many2one(
        'stock.location', string='Ubicación')

    @api.depends('fedor_location_id')
    def _getlocationline(self):
        for line in self:
            line.fedor_location_id = ""
            for line_location in line.move_line_ids:
                if (line_location.location_id):
                    line.fedor_location_id = line_location.location_id
                    line.fedor_location_store_id = line.fedor_location_id

    @api.model
    def create(self, vals):
        records = super().create(vals)
        for line in records:
            for pack in line.product_id.packaging_ids:
                if (pack.id == line.product_packaging_id.id):
                    _logger.info("--Quantity:--"+str(line.availability))
                    _logger.info("--Quantity-:--"+str(pack.qty))
                    line.fedor_product_packaging_qty = line.availability / pack.qty

        return records

    @api.onchange('quantity')
    def _onchange_quantity(self):
        for line in self:
            for pack in line.product_id.packaging_ids:
                if (pack.name == line.product_packaging_id.name):
                    line.fedor_product_packaging_qty = line.quantity/pack.qty

    # @api.onchange('fedor_product_packaging_qty')
    # def _change_fedor_product_packaging_qty(self):
    #     for line in self:
    #         if (line.fedor_product_packaging_qty != 0):
    #             qty = 0
    #             for line in line.picking_id.move_ids:
    #                 qty += line.fedor_product_packaging_qty
    #             if (qty != 0):
    #                 line.picking_id.fedor_product_packaging_qty = qty
