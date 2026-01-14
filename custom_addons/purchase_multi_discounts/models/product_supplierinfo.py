
# -*- coding: utf-8 -*-
# Part of AlmightyCS. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    multi_discount = fields.Char('Discounts')

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
