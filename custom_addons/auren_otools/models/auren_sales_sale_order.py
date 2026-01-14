from odoo import Command, _, api, fields, models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from collections import defaultdict
import logging
_logger = logging.getLogger(__name__)


class AurenSalesSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _auren_otools_change_partner_id(self):
        self._add_update_discount_head(True)

    @api.onchange('order_line')
    def _auren_otools_change_order_line(self):
        self._add_update_discount_head(False)

    def _add_update_discount_head(self, create_line):

        parameters = self.env['ir.config_parameter'].sudo()
        group_extended_discount = self.env.user.has_group(
            'auren_otools.group_head_extended_discount')

        if (group_extended_discount):

            sequence = 0
            disc_1 = False
            disc_2 = False
            disc_3 = False
            disc_4 = False
            disc_5 = False
            disc_6 = False
            for order in self:
                for line in order.order_line:
                    if (sequence < line.sequence):
                        sequence = line.sequence
                    if (line.type_disc == "disc_1"):
                        disc_1 = line
                    if (line.type_disc == "disc_2"):
                        disc_2 = line
                    if (line.type_disc == "disc_3"):
                        disc_3 = line
                    if (line.type_disc == "disc_4"):
                        disc_4 = line
                    if (line.type_disc == "disc_5"):
                        disc_5 = line
                    if (line.type_disc == "disc_6"):
                        disc_6 = line
                if (order.partner_id.disc_head_1 != False):
                    discount_percent = order.partner_id.disc_head_1/100
                    order._create_update_discount_lines(
                        discount_percent, "1", "disc_1", sequence+1, disc_1, create_line)

                if (order.partner_id.disc_head_2 != False):
                    discount_percent = order.partner_id.disc_head_2/100
                    order._create_update_discount_lines(
                        discount_percent, "2", "disc_2", sequence+1, disc_2, create_line)
                if (order.partner_id.disc_head_3 != False):
                    discount_percent = order.partner_id.disc_head_3/100
                    order._create_update_discount_lines(
                        discount_percent, "3", "disc_3", sequence+1, disc_3, create_line)

                if (order.partner_id.disc_head_4 != False):
                    discount_percent = order.partner_id.disc_head_4/100
                    order._create_update_discount_lines(
                        discount_percent, "4", "disc_4", sequence+1, disc_4, create_line)
                if (order.partner_id.disc_head_5 != False):
                    discount_percent = order.partner_id.disc_head_5/100
                    order._create_update_discount_lines(
                        discount_percent, "5", "disc_5", sequence+1, disc_5, create_line)
                if (order.partner_id.disc_head_6 != False):
                    discount_percent = order.partner_id.disc_head_6/100
                    order._create_update_discount_lines(
                        discount_percent, "6", "disc_6", sequence+1, disc_6, create_line)

    def _create_update_discount_lines(self, discount_percentage, number_disc, type_disc, sequence, line_disc, create_line):
        self.ensure_one()
        parameters = self.env['ir.config_parameter'].sudo()
        action_disc = parameters.get_param(
            'auren_otools.operation_head_discount'+number_disc)
        desc_disc = parameters.get_param(
            'auren_otools.desc_group_head_extended_discount_'+number_disc)
        discount_product = parameters.get_param(
            'auren_otools.product_discount_'+number_disc+'_id')

        add_vat_line_discount = parameters.get_param(
            'auren_otools.add_vat_line_discount')
        group_head_extended_discount_num = self.env.user.has_group(
            'auren_otools.group_head_extended_discount_'+number_disc)
        sub_total_order = self._get_total(type_disc)
        if (line_disc != False):
            for taxes, subtotal in sub_total_order.items():
                imp_sub = 0
                if (action_disc == "dec"):
                    imp_sub = -subtotal
                else:
                    imp_sub = subtotal
                line_disc.price_unit = imp_sub*discount_percentage
                line_disc.sequence = sequence+1
                if (add_vat_line_discount):
                    line_disc.tax_id = taxes.ids
        else:

            if (create_line):
                if (group_head_extended_discount_num):
                    # product_id = self.sudo().env['product.template'].browse(
                    #     int(discount_product))
                    product_id = self.sudo().env['product.product'].browse(
                        int(discount_product))

                    if (product_id != False):

                        vals_list = []
                        vals_list.append((0, 0, self._prepare_discount_line_values(
                            product=product_id,
                            amount=0,
                            taxes=False,
                            type_disc=type_disc, action_disc=action_disc, sequence=sequence,
                            description=_(
                                "%(desc_disc)s: %(percent)s%% ",
                                percent=discount_percentage*100,
                                desc_disc=desc_disc,
                            ),
                        )))
                        # for taxes, subtotal in sub_total_order.items():
                        #     vals_list.append((0, 0, self._prepare_discount_line_values(
                        #         product=product_id,
                        #         amount=subtotal * discount_percentage,
                        #         taxes=taxes,
                        #         type_disc=type_disc, action_disc=action_disc, sequence=sequence,
                        #         description=_(
                        #             "%(desc_disc)s: %(percent)s%% - On products with the following taxes %(taxes)s",
                        #             percent=discount_percentage*100,
                        #             taxes=", ".join(taxes.mapped('name')),
                        #             desc_disc=desc_disc,
                        #         ),
                        #     )))

                        self.order_line = vals_list
                    # return self.sudo().env['sale.order.line'].create(vals_list)

    def _get_total(self, type_desc):
        total_price_per_tax_groups = defaultdict(float)
        for line in self.order_line:
            if not line.product_uom_qty or not line.price_unit:
                continue
            if (line.type_disc == False):
                total_price_per_tax_groups[line.tax_id] += line.price_subtotal
            else:
                if (line.type_disc[5:6] < type_desc[5:6]):
                    total_price_per_tax_groups[line.tax_id] += line.price_subtotal
        return total_price_per_tax_groups

    def _prepare_discount_line_values(self, product, amount, taxes, type_disc, action_disc, sequence, description=None):
        self.ensure_one()
        imp = 0
        if (action_disc == "dec"):
            imp = -amount
        else:
            imp = amount
        if (taxes == False):
            vals = {
                'product_id': product.id,
                'product_uom_qty': 1,
                'sequence': sequence,
                'order_id': self.id,
                'price_unit': imp,
                'type_disc': type_disc,
            }
        else:
            vals = {
                'product_id': product.id,
                'product_uom_qty': 1,
                'sequence': sequence,
                'order_id': self.id,
                'price_unit': imp,
                'tax_id': taxes.ids,
                'type_disc': type_disc,
            }

        if description:
            vals['name'] = description

        return vals
