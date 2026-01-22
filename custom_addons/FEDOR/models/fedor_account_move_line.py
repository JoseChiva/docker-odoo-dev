# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models, api
from odoo.tools import formatLang, format_date

from markupsafe import Markup, escape


class FedorAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('currency_id', 'company_id', 'move_id.date')
    def _compute_currency_rate(self):
        currency_rate_standard = super()._compute_currency_rate()
        for line in self:
            if (line.move_id.currency_rate):
                line.currency_rate = 1/line.move_id.currency_rate
