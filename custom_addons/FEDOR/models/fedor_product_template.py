from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class FedorProductTemplate(models.Model):
    _inherit = "product.template"

    product_family_id = fields.Many2one(
        'fedor.product.family', 'Familia',
    )
    type_id = fields.Many2one(
        'fedor.type', 'Tipo',
    )

    is_item_catalogue = fields.Boolean(
        default=True, string="Es artículo de catalogo?")

    sale_minim_qty = fields.Float(string='Cantidad mínima de venta')

    volume = fields.Float(digits=(16, 6))
