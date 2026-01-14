from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _

from collections import defaultdict


class AurenSalesSaleOrder(models.Model):
    _inherit = 'sale.order.line'

    disc_1 = fields.Float('Descuento 1', default=0)
    disc_2 = fields.Float('Descuento 2', default=0)
    disc_3 = fields.Float('Descuento 3', default=0)
    disc_4 = fields.Float('Descuento 4', default=0)
    disc_5 = fields.Float('Descuento 5', default=0)
    disc_6 = fields.Float('Descuento 6', default=0)

    @api.onchange('disc_1', 'disc_2', 'disc_3', 'disc_4', 'disc_5', 'disc_6')
    def _change_discount(self):
        for order_line in self:
            order_line._compute_amount()
            order_line.apply_discount_percent(order_line)

    def _convert_to_tax_base_line_dict(self, **kwargs):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.order_id.currency_id,
            product=self.product_id,
            taxes=self.tax_id,
            price_unit=self.apply_discount_price(self),
            quantity=self.product_uom_qty,
            discount=self.discount,
            price_subtotal=self.price_subtotal,
            **kwargs,
        )

        # for order_line in self:
        # super()._compute_amount()
        # order_line.apply_descount(order_line)

    def apply_discount_percent(self, order_line):
        parameters = self.env['ir.config_parameter'].sudo()
        type_discount = parameters.get_param(
            'auren_otools.type_discount')

        group_extended_discount = parameters.get_param(
            'auren_otools.group_extended_discount')
        if (group_extended_discount):
            if (type_discount == "sum"):
                group_extended_discount_1 = parameters.get_param(
                    'auren_otools.group_extended_discount_1')
                group_extended_discount_2 = parameters.get_param(
                    'auren_otools.group_extended_discount_2')
                group_extended_discount_3 = parameters.get_param(
                    'auren_otools.group_extended_discount_3')
                group_extended_discount_4 = parameters.get_param(
                    'auren_otools.group_extended_discount_4')
                group_extended_discount_5 = parameters.get_param(
                    'auren_otools.group_extended_discount_5')
                group_extended_discount_6 = parameters.get_param(
                    'auren_otools.group_extended_discount_6')

                discount = 0
                if (group_extended_discount_1):
                    discount = discount + order_line.disc_1
                if (group_extended_discount_2):
                    discount = discount + order_line.disc_2
                if (group_extended_discount_3):
                    discount = discount + order_line.disc_3
                if (group_extended_discount_4):
                    discount = discount + order_line.disc_4
                if (group_extended_discount_5):
                    discount = discount + order_line.disc_5
                if (group_extended_discount_6):
                    discount = discount + order_line.disc_6
                if (discount > 0):
                    order_line.discount = discount

    def apply_discount_price(self, order_line):
        parameters = self.env['ir.config_parameter'].sudo()
        type_discount = parameters.get_param(
            'auren_otools.type_discount')
        if (type_discount == "app"):
            group_extended_discount_1 = parameters.get_param(
                'auren_otools.group_extended_discount_1')
            group_extended_discount_2 = parameters.get_param(
                'auren_otools.group_extended_discount_2')
            group_extended_discount_3 = parameters.get_param(
                'auren_otools.group_extended_discount_3')
            group_extended_discount_4 = parameters.get_param(
                'auren_otools.group_extended_discount_4')
            group_extended_discount_5 = parameters.get_param(
                'auren_otools.group_extended_discount_5')
            group_extended_discount_6 = parameters.get_param(
                'auren_otools.group_extended_discount_6')

            price_unit = order_line.price_unit

            if (group_extended_discount_1):
                price_unit = (price_unit*(1-(order_line.disc_1/100)))
            if (group_extended_discount_2):
                price_unit = (price_unit*(1-(order_line.disc_2/100)))
            if (group_extended_discount_3):
                price_unit = (price_unit*(1-(order_line.disc_3/100)))
            if (group_extended_discount_4):
                price_unit = (price_unit*(1-(order_line.disc_4/100)))
            if (group_extended_discount_5):
                price_unit = (price_unit*(1-(order_line.disc_5/100)))
            if (group_extended_discount_6):
                price_unit = (price_unit*(1-(order_line.disc_6/100)))

            return price_unit
        else:
            order_line.price_unit

    @api.onchange('product_template_id')
    def _load_discount_res_partner(self):
        for order_line in self:
            order_line.disc_1 = order_line.order_id.partner_id.disc_1
            order_line.disc_2 = order_line.order_id.partner_id.disc_2
            order_line.disc_3 = order_line.order_id.partner_id.disc_3
            order_line.disc_4 = order_line.order_id.partner_id.disc_4
            order_line.disc_5 = order_line.order_id.partner_id.disc_5
            order_line.disc_6 = order_line.order_id.partner_id.disc_6
