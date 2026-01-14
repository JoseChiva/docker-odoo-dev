from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class AurenSaleResPartners(models.Model):
    _inherit = "res.partner"

    disc_1 = fields.Float('Descuento 1', default=0)
    disc_2 = fields.Float('Descuento 2', default=0)
    disc_3 = fields.Float('Descuento 3', default=0)
    disc_4 = fields.Float('Descuento 4', default=0)
    disc_5 = fields.Float('Descuento 5', default=0)
    disc_6 = fields.Float('Descuento 6', default=0)

    disc_head_1 = fields.Float('Cabecera Descuento 1', default=0)
    disc_head_2 = fields.Float('Cabecera Descuento 2', default=0)
    disc_head_3 = fields.Float('Cabecera Descuento 3', default=0)
    disc_head_4 = fields.Float('Cabecera Descuento 4', default=0)
    disc_head_5 = fields.Float('Cabecera Descuento 5', default=0)
    disc_head_6 = fields.Float('Cabecera Descuento 6', default=0)

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            name_var1 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_1')
            if (name_var1 != False):
                for node in arch.xpath(
                    "//field[@name='disc_1']"
                ):
                    node.attrib['string'] = name_var1

            name_var2 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_2')
            if (name_var2 != False):
                for node in arch.xpath(
                    "//field[@name='disc_2']"
                ):
                    node.attrib['string'] = name_var2

            name_var3 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_3')
            if (name_var3 != False):
                for node in arch.xpath(
                    "//field[@name='disc_3']"
                ):
                    node.attrib['string'] = name_var3

            name_var4 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_4')
            if (name_var4 != False):
                for node in arch.xpath(
                    "//field[@name='disc_4']"
                ):
                    node.attrib['string'] = name_var4

            name_var5 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_5')
            if (name_var5 != False):
                for node in arch.xpath(
                    "//field[@name='disc_5']"
                ):
                    node.attrib['string'] = name_var5

            name_var6 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_6')
            if (name_var6 != False):
                for node in arch.xpath(
                    "//field[@name='disc_6']"
                ):
                    node.attrib['string'] = name_var6

            name_head_var1 = parameters.get_param(
                'multi_discount_sale.desc_group_head_extended_discount_1')
            if (name_head_var1 != False):
                for node in arch.xpath(
                    "//field[@name='disc_head_1']"
                ):
                    node.attrib['string'] = name_head_var1

            name_head_var2 = parameters.get_param(
                'multi_discount_sale.desc_group_head_extended_discount_2')
            if (name_head_var2 != False):
                for node in arch.xpath(
                    "//field[@name='disc_head_2']"
                ):
                    node.attrib['string'] = name_head_var2

            name_head_var3 = parameters.get_param(
                'multi_discount_sale.desc_group_head_extended_discount_3')
            if (name_head_var3 != False):
                for node in arch.xpath(
                    "//field[@name='disc_head_3']"
                ):
                    node.attrib['string'] = name_head_var3

            name_head_var4 = parameters.get_param(
                'multi_discount_sale.desc_group_head_extended_discount_4')
            if (name_head_var4 != False):
                for node in arch.xpath(
                    "//field[@name='disc_head_4']"
                ):
                    node.attrib['string'] = name_head_var4

            name_head_var5 = parameters.get_param(
                'multi_discount_sale.desc_group_head_extended_discount_5')
            if (name_head_var5 != False):
                for node in arch.xpath(
                    "//field[@name='disc_head_5']"
                ):
                    node.attrib['string'] = name_head_var5

            name_head_var6 = parameters.get_param(
                'multi_discount_sale.desc_group_head_extended_discount_6')
            if (name_head_var6 != False):
                for node in arch.xpath(
                    "//field[@name='disc_head_6']"
                ):
                    node.attrib['string'] = name_head_var6
        return arch, view
