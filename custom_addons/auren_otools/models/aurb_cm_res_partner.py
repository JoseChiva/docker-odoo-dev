from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmResPartner(models.Model):
    _inherit = "res.partner"

    authorized_sales = fields.Boolean(
        default=False, string="Comprador registrado")

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            sale_autorization_management = parameters.get_param(
                'auren_otools.sale_autorization_management')
            if (sale_autorization_management == False):
                for node in arch.xpath(
                    "//field[@name='authorized_sales']"
                ):
                    node.attrib['invisible'] = '1'

        return arch, view
