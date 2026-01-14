from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmSaleOrder(models.Model):
    _inherit = "sale.order"

    res_partner_authorized_sales = fields.Many2one("res.partner", string="Comprador registrado",
                                                   domain="[('is_company','=',False),('type','=','contact'),('authorized_sales','=',True),('parent_id.id','=',partner_id)]")

    res_partner_contact = fields.Many2one("res.partner", string="Persona de contacto",
                                          domain="[('is_company','=',False),('type','=','contact'),('parent_id.id','=',partner_id)]")

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            group_extended_discount = self.env.user.has_group(
                'auren_otools.group_extended_discount')
            if (group_extended_discount):
                for node in arch.xpath(
                    "//field[@name='discount']"
                ):
                    node.attrib['column_invisible'] = "1"

            name_var1 = parameters.get_param(
                'auren_otools.var1_s')
            name_var2 = parameters.get_param(
                'auren_otools.var2_s')
            name_var3 = parameters.get_param(
                'auren_otools.var3_s')

            if (name_var1 != False):
                for node in arch.xpath(
                    "//field[@name='var1']"
                ):
                    node.attrib['string'] = name_var1
            if (name_var2 != False):
                for node in arch.xpath(
                    "//field[@name='var2']"
                ):
                    node.attrib['string'] = name_var2
            if (name_var3 != False):
                for node in arch.xpath(
                    "//field[@name='var3']"
                ):
                    node.attrib['string'] = name_var3

            var_readonly = parameters.get_param(
                'auren_otools.var_readonly_s')
            if (var_readonly):
                for node in arch.xpath(
                    "//field[@name='var1']"
                ):
                    node.attrib['readonly'] = '1'
                for node in arch.xpath(
                    "//field[@name='var2']"
                ):
                    node.attrib['readonly'] = '1'
                for node in arch.xpath(
                    "//field[@name='var3']"
                ):
                    node.attrib['readonly'] = '1'

            sale_autorization_management = parameters.get_param(
                'auren_otools.sale_autorization_management')
            if (sale_autorization_management == False):
                for node in arch.xpath(
                    "//field[@name='res_partner_authorized_sales']"
                ):
                    node.attrib['invisible'] = '1'

            name_var1 = parameters.get_param(
                'auren_otools.desc_group_extended_discount_1')
            if (name_var1 != False):
                for node in arch.xpath(
                    "//field[@name='disc_1']"
                ):
                    node.attrib['string'] = name_var1

            name_var2 = parameters.get_param(
                'auren_otools.desc_group_extended_discount_2')
            if (name_var2 != False):
                for node in arch.xpath(
                    "//field[@name='disc_2']"
                ):
                    node.attrib['string'] = name_var2

            name_var3 = parameters.get_param(
                'auren_otools.desc_group_extended_discount_3')
            if (name_var3 != False):
                for node in arch.xpath(
                    "//field[@name='disc_3']"
                ):
                    node.attrib['string'] = name_var3

            name_var4 = parameters.get_param(
                'auren_otools.desc_group_extended_discount_4')
            if (name_var4 != False):
                for node in arch.xpath(
                    "//field[@name='disc_4']"
                ):
                    node.attrib['string'] = name_var4

            name_var5 = parameters.get_param(
                'auren_otools.desc_group_extended_discount_5')
            if (name_var5 != False):
                for node in arch.xpath(
                    "//field[@name='disc_5']"
                ):
                    node.attrib['string'] = name_var5

            name_var6 = parameters.get_param(
                'auren_otools.desc_group_extended_discount_6')
            if (name_var6 != False):
                for node in arch.xpath(
                    "//field[@name='disc_6']"
                ):
                    node.attrib['string'] = name_var6

        return arch, view
