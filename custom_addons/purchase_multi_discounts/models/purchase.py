# -*- coding: utf-8 -*-
# Part of AlmightyCS. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _total_discount(self):
        for rec in self:
            discount_amount = 0
            for line in rec.order_line:
                discount_amount += line.discount_amount
            rec.discount_amount = discount_amount
            rec.avg_discount = (discount_amount*100) / \
                rec.amount_untaxed if rec.amount_untaxed else 0

    discount_amount = fields.Float(
        'Total Discount', compute="_total_discount", digits=('Discount'))
    avg_discount = fields.Float(
        'Avg Discount', compute="_total_discount", digits=('Discount'))
    print_discount = fields.Boolean('Print Discount')
    print_discount_amount = fields.Boolean('Print Discount Amount')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _compute_price_unit_and_date_planned_and_name(self):
        super(PurchaseOrderLine, self)._compute_price_unit_and_date_planned_and_name()
        for line in self:
            if not line.product_id or line.invoice_lines or not line.company_id:
                continue
            params = line._get_select_sellers_params()
            seller = line.product_id._select_seller(
                partner_id=line.partner_id,
                quantity=line.product_qty,
                date=line.order_id.date_order and line.order_id.date_order.date(
                ) or fields.Date.context_today(line),
                uom_id=line.product_uom,
                params=params)
            if seller:
                if (seller.multi_discount):
                    line.multi_discount = seller.multi_discount

    def _total_discount(self):
        for rec in self:
            discount = ((rec.discount*rec.price_unit)/100)
            rec.discount_per_unit = discount
            rec.discount_amount = discount*rec.product_qty
            rec.discounted_unit_price = rec.price_unit - discount

    discount_amount = fields.Float(
        'Discount Amount', compute="_total_discount", digits=('Discount'))
    discount_per_unit = fields.Float(
        'Discount Per Unit', compute="_total_discount", digits=('Discount'))
    multi_discount = fields.Char('Discounts')
    discounted_unit_price = fields.Float(
        'Discounted Unit Price', compute="_total_discount", digits=('Discount'))

    @api.onchange('multi_discount')
    def _onchange_multi_discount(self):
        def get_disocunt(percentage, amount):
            new_amount = (percentage * amount)/100
            return (amount - new_amount)
        if self.multi_discount:
            amount = 100
            splited_discounts = self.multi_discount.split("+")
            for disocunt in splited_discounts:
                amount = get_disocunt(float(disocunt), amount)
            self.discount = 100 - amount
        else:
            self.discount = 0
