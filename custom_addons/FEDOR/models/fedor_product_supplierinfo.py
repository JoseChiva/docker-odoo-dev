
from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class FedorproductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    type_change = fields.Float(string='Tipo de cambio', digits=(16, 6),)
    expenses_percent = fields.Float(string='% Gastos')
    expenses_fixed = fields.Float(string='Gastos Fijos')
    cost_product = fields.Float(
        string='Coste', compute="_compute_cost_product")

    def _compute_cost_product(self):
        for product_supplierinfo in self:
            if (product_supplierinfo.product_tmpl_id):
                product_supplierinfo.cost_product = product_supplierinfo.product_tmpl_id.standard_price
