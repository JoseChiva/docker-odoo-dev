from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class SucoPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    price_base = fields.Float(string="Precio base")
    add_price_unit = fields.Float(string="Inc. unit.")

    @api.onchange('add_price_unit')
    def change_add_price_unit(self):
        if (self.add_price_unit):
            if (self.price_base):
                if (self.product_uom_qty):
                    self.price_unit = self.price_base + \
                        (self.add_price_unit)

    def _compute_price_unit_and_date_planned_and_name(self):
        super()._compute_price_unit_and_date_planned_and_name()
        for line in self:
            line.price_base = line.price_unit
            if (line.price_base):
                line.price_unit = line.price_base + \
                    (line.add_price_unit)
