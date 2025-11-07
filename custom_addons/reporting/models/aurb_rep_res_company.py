from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbRepResCompany(models.Model):
    _inherit = "res.company"

    commercial_registry = fields.Text(string="registro mercantil")
    generic_text_1_delivery = fields.Text(string="Texto genérico 1 albarán")
    generic_text_2_delivery = fields.Text(string="Texto genérico 2 albarán")
