from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurenExUomProductTemplate(models.Model):
    _inherit = "product.template"

    uom_sale_factor_ids = fields.One2many(
        "auren.exuom.product.uom.sale", 'product_id')
    uom_purchase_factor_ids = fields.One2many(
        "auren.exuom.product.uom.purchase", 'product_id')

    uom_scandal_factor_ids = fields.One2many(
        "auren.exuom.product.uom.scandal", 'product_id')

    var1_s = fields.Float(string="var1")
    var2_s = fields.Float(string="var2")
    var3_s = fields.Float(string="var3")

    uom_sale_id = fields.Many2one("uom.uom",
                                  help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.")

    uom_scandal_id = fields.Many2one("uom.uom",
                                     help="Default unit of measure used for Scandal. It must be in the same category as the default unit of measure.")

    @api.onchange('uom_sale_id')
    def _onchange_uom(self):
        if self.uom_sale_id and self.uom_id and self.uom_sale_id.category_id != self.uom_id.category_id:
            self.uom_sale_id = self.uom_id

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            # Compras

            # Ventas

            name_var1_s = parameters.get_param(
                'extended_uom.var1_s')
            name_var2_s = parameters.get_param(
                'extended_uom.var2_s')
            name_var3_s = parameters.get_param(
                'extended_uom.var3_s')
            if (name_var1_s != False):
                for node in arch.xpath(
                    "//field[@name='var1_s']"
                ):
                    node.attrib['string'] = name_var1_s
            if (name_var2_s != False):
                for node in arch.xpath(
                    "//field[@name='var2_s']"
                ):
                    node.attrib['string'] = name_var2_s
            if (name_var3_s != False):
                for node in arch.xpath(
                    "//field[@name='var3_s']"
                ):
                    node.attrib['string'] = name_var3_s

        return arch, view
