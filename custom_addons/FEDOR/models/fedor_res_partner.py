from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class FedorResPartner(models.Model):
    _inherit = "res.partner"

    type_id = fields.Many2one(
        'fedor.type', 'Tipo',
    )
