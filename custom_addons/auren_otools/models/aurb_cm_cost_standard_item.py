from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmCostStandardItem(models.Model):
    _name = "aurb.cm.cost.standard.item"
    _description = "Aurb Cost Standard Item"

    product_id = fields.Many2one("product.template")
    cost_standard_id = fields.Many2one("aurb.cm.cost.standard")

    cost = fields.Float(string="Cost")
