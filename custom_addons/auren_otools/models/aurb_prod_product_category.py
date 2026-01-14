from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmProductTemplate(models.Model):
    _inherit = "product.category"
    extended_ean_product = fields.Boolean(
        string="Gestión EAN automático por categoría",
    )
    extended_ean_product_counter = fields.Integer(
        string="Contador",
    )
