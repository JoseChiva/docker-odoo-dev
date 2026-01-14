from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurenSaleAccountMoveLine(models.Model):
    _inherit = "account.move.line"

    type_disc = fields.Char(string="type_disc")

    disc_1 = fields.Float('Descuento 1', default=0)
    disc_2 = fields.Float('Descuento 2', default=0)
    disc_3 = fields.Float('Descuento 3', default=0)
    disc_4 = fields.Float('Descuento 4', default=0)
    disc_5 = fields.Float('Descuento 5', default=0)
    disc_6 = fields.Float('Descuento 6', default=0)

    @api.onchange('disc_1', 'disc_2', 'disc_3', 'disc_4', 'disc_5', 'disc_6')
    def _change_discount(self):
        for order_line in self:
            # order_line._compute_amount()
            order_line.apply_discount_percent(order_line)

    def apply_discount_percent(self, order_line):
        parameters = self.env['ir.config_parameter'].sudo()
        type_discount = parameters.get_param(
            'multi_discount_sale.type_discount')

        group_extended_discount = self.env.user.has_group(
            'multi_discount_sale.group_extended_discount')
        if (group_extended_discount):

            operation_discount_1 = parameters.get_param(
                'multi_discount_sale.operation_discount_1')
            operation_discount_2 = parameters.get_param(
                'multi_discount_sale.operation_discount_2')
            operation_discount_3 = parameters.get_param(
                'multi_discount_sale.operation_discount_3')
            operation_discount_4 = parameters.get_param(
                'multi_discount_sale.operation_discount_4')
            operation_discount_5 = parameters.get_param(
                'multi_discount_sale.operation_discount_5')
            operation_discount_6 = parameters.get_param(
                'multi_discount_sale.operation_discount_6')

            if (type_discount == "sum"):
                group_extended_discount_1 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_1')
                group_extended_discount_2 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_2')
                group_extended_discount_3 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_3')
                group_extended_discount_4 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_4')
                group_extended_discount_5 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_5')
                group_extended_discount_6 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_6')

                discount = 0
                if (group_extended_discount_1):
                    if (order_line.disc_1):
                        if (operation_discount_1 == "dec"):
                            discount = discount + order_line.disc_1
                        else:
                            discount = discount - order_line.disc_1
                if (group_extended_discount_2):
                    if (order_line.disc_2):
                        if (operation_discount_2 == "dec"):
                            discount = discount + order_line.disc_2
                        else:
                            discount = discount - order_line.disc_2
                if (group_extended_discount_3):
                    if (order_line.disc_3):
                        if (operation_discount_3 == "dec"):
                            discount = discount + order_line.disc_3
                        else:
                            discount = discount - order_line.disc_3
                if (group_extended_discount_4):
                    if (order_line.disc_4):
                        if (operation_discount_4 == "dec"):
                            discount = discount + order_line.disc_4
                        else:
                            discount = discount - order_line.disc_4
                if (group_extended_discount_5):
                    if (order_line.disc_5):
                        if (operation_discount_5 == "dec"):
                            discount = discount + order_line.disc_5
                        else:
                            discount = discount - order_line.disc_5
                if (group_extended_discount_6):
                    if (order_line.disc_6):
                        if (operation_discount_6 == "dec"):
                            discount = discount + order_line.disc_6
                        else:
                            discount = discount - order_line.disc_6
                if (discount > 0):
                    order_line.discount = discount
            elif (type_discount == "app"):
                group_extended_discount_1 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_1')
                group_extended_discount_2 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_2')
                group_extended_discount_3 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_3')
                group_extended_discount_4 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_4')
                group_extended_discount_5 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_5')
                group_extended_discount_6 = self.env.user.has_group(
                    'multi_discount_sale.group_extended_discount_6')
                discount = 0
                # order_line.discount = discount
                if (group_extended_discount_1):
                    if (order_line.disc_1):
                        if (operation_discount_1 == "dec"):
                            discount = (1 - 0.01*order_line.disc_1)
                        else:
                            discount = (1 + 0.01*order_line.disc_1)

                if (group_extended_discount_2):
                    if (order_line.disc_2):
                        if (operation_discount_2 == "dec"):
                            discount = discount*(1 - 0.01*order_line.disc_2)
                        else:
                            discount = discount*(1 + 0.01*order_line.disc_2)
                if (group_extended_discount_3):
                    if (order_line.disc_3):
                        if (operation_discount_3 == "dec"):
                            discount = discount*(1 - 0.01*order_line.disc_3)
                        else:
                            discount = discount*(1 + 0.01*order_line.disc_3)
                if (group_extended_discount_4):
                    if (order_line.disc_4):
                        if (operation_discount_4 == "dec"):
                            discount = discount*(1 - 0.01*order_line.disc_4)
                        else:
                            discount = discount*(1 + 0.01*order_line.disc_4)
                if (group_extended_discount_5):
                    if (order_line.disc_5):
                        if (operation_discount_5 == "dec"):
                            discount = discount*(1 - 0.01*order_line.disc_5)
                        else:
                            discount = discount*(1 + 0.01*order_line.disc_5)
                if (group_extended_discount_6):
                    if (order_line.disc_6):
                        if (operation_discount_6 == "dec"):
                            discount = discount*(1 - 0.01*order_line.disc_6)
                        else:
                            discount = discount*(1 + 0.01*order_line.disc_6)
                if (discount > 0):
                    order_line.discount = 100-(100*discount)

    @api.onchange('product_id')
    def _load_discount_res_partner(self):
        for order_line in self:
            order_line.disc_1 = order_line.move_id.partner_id.disc_1
            order_line.disc_2 = order_line.move_id.partner_id.disc_2
            order_line.disc_3 = order_line.move_id.partner_id.disc_3
            order_line.disc_4 = order_line.move_id.partner_id.disc_4
            order_line.disc_5 = order_line.move_id.partner_id.disc_5
            order_line.disc_6 = order_line.move_id.partner_id.disc_6
            order_line.apply_discount_percent(order_line)
