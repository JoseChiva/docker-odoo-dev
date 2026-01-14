from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurenExUomSaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            name_var1 = parameters.get_param(
                'extended_uom.var1_s')
            name_var2 = parameters.get_param(
                'extended_uom.var2_s')
            name_var3 = parameters.get_param(
                'extended_uom.var3_s')

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
                'extended_uom.var_readonly_s')
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

        return arch, view
