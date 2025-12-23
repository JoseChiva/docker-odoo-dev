from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class SucoSaleOrder(models.Model):
    _inherit = "sale.order"
