from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class FedorProductPriceList(models.Model):
    _inherit = "product.pricelist"

    code = fields.Char(index=True, string="Código")
