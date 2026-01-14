# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models, api
from odoo.tools import formatLang, format_date

from markupsafe import Markup, escape


class AurenAccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def write(self, vals):
        for account_move in self:
            if 'state' in vals and vals['state'] == 'posted' and account_move.state == 'draft':
                if (account_move.move_type in ['out_invoice', 'in_invoice', 'out_refund']):
                    account_move.auren_make_commission()
        return super(AurenAccountMove, self).write(vals)

    def _make_commission(self):
        # cancelamos el evento de generación de comision al cobrar la factura
        # ya que se esta generando al crear la factura

        x = 0
        # super()._make_commission()

    def auren_make_commission(self):
        for move in self.filtered(lambda m: m.move_type in ['out_invoice', 'in_invoice', 'out_refund']):
            if move.move_type in ['out_invoice', 'in_invoice']:
                sign = 1
                if move.commission_po_line_id or not move.referrer_id:
                    continue
            else:
                sign = -1
                if not move.commission_po_line_id:
                    continue

            comm_by_rule = defaultdict(float)

            product = None
            order = None
            desc_lines = ""
            for line in move.invoice_line_ids:
                rule = line._get_commission_rule()
                if rule:
                    if not product:
                        product = rule.plan_id.product_id
                    if not order:
                        order = line.subscription_id
                        desc_lines += _("\n%s: from %s to %s", line.product_id.name, format_date(self.env, line.deferred_start_date),
                                        format_date(self.env, line.deferred_end_date))

                    if (line.sale_line_ids.manual_commission):
                        commission = move.currency_id.round(
                            line.price_subtotal * line.sale_line_ids.commission / 100.0)
                    else:
                        commission = move.currency_id.round(
                            line.price_subtotal * rule.rate / 100.0)

                    comm_by_rule[rule] += commission

            # regulate commissions
            for r, amount in comm_by_rule.items():
                if r.is_capped:
                    amount = min(amount, r.max_commission)
                    comm_by_rule[r] = amount

            total = sum(comm_by_rule.values())
            if not total:
                continue

            # build description lines
            desc = _(
                'Commission on %(invoice)s, %(partner)s, %(amount)s',
                invoice=move.invoice_origin,
                partner=move.partner_id.name,
                amount=formatLang(self.env, move.amount_untaxed,
                                  currency_obj=move.currency_id),
            )
            # desc = _(
            #     'Commission on %(invoice)s, %(partner)s, %(amount)s',
            #     invoice=move.name,
            #     partner=move.partner_id.name,
            #     amount=formatLang(self.env, move.amount_untaxed,
            #                       currency_obj=move.currency_id),
            # )
            if order:
                desc += f"\n{order.name}, {desc_lines}"
                # extend the description to show the number of months to defer the expense over
                end_date_list = move.invoice_line_ids.mapped(
                    'deferred_end_date')
                start_date_list = move.invoice_line_ids.mapped(
                    'deferred_start_date')
                date_to = max([ed for ed in end_date_list if ed])
                date_from = min([sd for sd in start_date_list if sd])
                # we calculate the delta according to the whole range to avoid 11 month and 29 days= 11 months
                delta = relativedelta(
                    date_to + relativedelta(days=1), date_from)
                n_months = delta.years * 12 + delta.months + delta.days // 30
                if n_months:
                    desc += _(' (%d month(s))', n_months)

            purchase = move._get_commission_purchase_order()

            line = self.env['purchase.order.line'].sudo().create({
                'name': desc,
                'product_id': product.id,
                'product_qty': 1,
                'price_unit': total * sign,
                'product_uom': product.uom_id.id,
                'date_planned': move.invoice_date,
                'order_id': purchase.id,
                'qty_received': 1,
            })

            if move.move_type in ['out_invoice', 'in_invoice']:
                # link the purchase order line to the invoice
                move.commission_po_line_id = line
                msg_body = _('New commission. Invoice: %s. Amount: %s.',
                             move._get_html_link(),
                             formatLang(self.env, total, currency_obj=move.currency_id))
            else:
                msg_body = _('Commission refunded. Invoice: %s. Amount: %s.',
                             move._get_html_link(),
                             formatLang(self.env, total, currency_obj=move.currency_id))
            purchase.message_post(body=msg_body)

    def _get_commission_purchase_order_domain(self):
        self.ensure_one()

        domain = [
            ('partner_id', '=', self.referrer_id.id),
            ('company_id', '=', self.company_id.id),
            ('state', '=', 'draft'),
            ('currency_id', '=', self.currency_id.id),
            ('purchase_type', '=', 'commission'),
        ]

        # Quitamos el dominio para que no cree diferentes compras segun el usuario que esta creando la venta
        # sales_rep = self._get_sales_representative()
        # if sales_rep:
        #     domain += [('user_id', '=', sales_rep.id)]

        return domain
