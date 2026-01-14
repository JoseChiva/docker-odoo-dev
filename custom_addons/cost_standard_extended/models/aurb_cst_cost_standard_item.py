from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCstCostStandardItem(models.Model):
    _name = "aurb.cst.cost.standard.item"
    _description = "Aurb Cost Standard Item"

    product_id = fields.Many2one("product.template")
    cost_standard_id = fields.Many2one("aurb.cst.cost.standard")

    cost = fields.Float(string="Cost")

    @api.onchange('cost_standard_id')
    def _onchange_cost_standard(self):
        for cost_item in self:
            if cost_item.cost_standard_id:
                if (cost_item.cost_standard_id.cost):
                    cost_item.cost = cost_item.cost_standard_id.cost
