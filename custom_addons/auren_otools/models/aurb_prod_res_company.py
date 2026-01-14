from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AurbProdResCompany(models.Model):
    _inherit = 'res.company'

    extended_ean_product = fields.Boolean(
        string="Gestión EAN automático",
        check_company=True,
    )

    extended_ean_product_country = fields.Char(string="Código pais",
                                               check_company=True,
                                               )
    extended_ean_product_company = fields.Char(string="Código Fabricante",
                                               check_company=True,
                                               )
    extended_ean_product_counter = fields.Integer(string="Contador",
                                                  check_company=True,
                                                  )
