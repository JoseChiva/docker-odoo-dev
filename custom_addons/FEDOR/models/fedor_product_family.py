from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime


class FedorProductFamily(models.Model):
    _name = 'fedor.product.family'
    _description = 'Familia de producto'
    _order = 'id'
    name = fields.Char(index=True, required=True, string="Nombre")
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    code = fields.Char(index=True, string="Código")

    is_family_catalogue = fields.Boolean(
        default=False, string="Es família de catalogo?")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.code != False:
                view_name = record.code+" - " + record.name
            record.display_name = view_name
