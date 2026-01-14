from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class AurenResPartner(models.Model):
    _inherit = "res.partner"

    referrer_id = fields.Many2one('res.partner', 'Representante', domain=[
        ('grade_id', '!=', False)])
