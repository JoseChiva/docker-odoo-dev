from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class SucoSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    price_base = fields.Float(string="Precio base")
    add_price_unit = fields.Float(string="Inc. unit.")

    @api.onchange('add_price_unit')
    def change_add_price_unit(self):
        if (self.add_price_unit):
            if (self.price_base):
                if (self.product_uom_qty):
                    self.price_unit = self.price_base + \
                        (self.add_price_unit)

    @api.onchange('product_id')
    def getpackingdefault(self):
        if self.product_id and self.product_id.packaging_ids:
            self.product_uom_qty = self.product_id.packaging_ids[0].qty
            self.product_packaging_id = self.product_id.packaging_ids[0].id
            self.product_packaging_qty = 1

    def _get_pricelist_price(self):
        for line in self:
            resultado = super()._get_pricelist_price()
            line.price_base = resultado
            if (line.add_price_unit):
                resultado += (line.add_price_unit)

        return resultado
