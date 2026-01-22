from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class FedorSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id')
    def getpackingdefault(self):
        for line in self:
            if (line.product_id):
                item = line.product_id
                if (item.packaging_ids):
                    line.product_uom_qty = item.packaging_ids[0].qty
                    line.product_packaging_id = item.packaging_ids[0].id
                    line.product_packaging_qty = 1
