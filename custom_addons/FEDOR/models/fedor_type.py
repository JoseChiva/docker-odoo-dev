from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime


class FedorType(models.Model):
    _name = 'fedor.type'
    _description = 'Tipo'
    _order = 'id'
    name = fields.Char(index=True, required=True, string="Nombre")
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    code = fields.Char(index=True, string="Código")
