from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmProductUomSale(models.Model):
    _name = "aurb.cm.product.uom.sale"
    _description = "Aurb Product Uom Sale"

    product_id = fields.Many2one("product.template")
    uom_id = fields.Many2one("uom.uom",
                             required=True,
                             help="Default unit of measure. It must be in the same category as the default unit of measure.")
    conversion_factor = fields.Float(
        string="Factor de conversión entre unidades", default=0, digits=(12, 8))
    unit__factor = fields.Float(
        "Factor de conversión dimensiones", default=0, digits=(12, 8))

    formula = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3"
    )

    # @api.onchange('product_id.uom_id')
    # def _onchange_product_uom(self):

    @api.onchange('uom_id')
    def _onchange_uom(self):
        if self.uom_id and self.product_id.uom_id and self.uom_id.category_id != self.product_id.uom_id.category_id:
            self.uom_id = self.product_id.uom_id
