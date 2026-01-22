from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _

from collections import defaultdict


class FedorSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _change_partner_id_fedor(self):
        for record in self:
            if (record.partner_id.referrer_id.id != False):
                record.referrer_id = record.partner_id.referrer_id.id

    def _compute_commission(self):
        self.commission = 0
        for so in self:
            if not so.referrer_id or not so.commission_plan_id:
                so.commission = 0
            else:
                comm_by_rule = defaultdict(float)
                template = so.sale_order_template_id
                template_id = template.id if template else None
                for line in so.order_line:
                    rule = so.commission_plan_id._match_rules(
                        line.product_id, template_id, so.pricelist_id.id)
                    if rule:
                        if (line.manual_commission == False):
                            line.commission = rule.rate
                        commission = so.currency_id.round(
                            line.price_subtotal * line.commission / 100.0)
                        comm_by_rule[rule] += commission

                # cap by rule
                for r, amount in comm_by_rule.items():
                    if r.is_capped:
                        amount = min(amount, r.max_commission)
                        comm_by_rule[r] = amount

                so.commission = sum(comm_by_rule.values())
