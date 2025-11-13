from odoo import models, fields

class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    gi_code_tarf = fields.Char(string="Código Tarifa")
    gi_name_tarf = fields.Char(string="Descripción Tarifa")
    gi_type = fields.Many2one('gi.type.price', string="Tipo de precio")