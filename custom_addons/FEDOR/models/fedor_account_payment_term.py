from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class FedorAccountPayment_term(models.Model):
    _inherit = "account.payment.term"

    code = fields.Char(index=True, string="Código")
