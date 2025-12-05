from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class AurbPedretProductPriceListItem(models.Model):
    _inherit = "product.pricelist.item"

    price_with_var1 = fields.Float()
    price_with_var2 = fields.Float()
    price_with_var3 = fields.Float()

    num_contract = fields.Char()
