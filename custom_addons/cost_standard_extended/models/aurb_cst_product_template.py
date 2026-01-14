from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCstProductTemplate(models.Model):
    _inherit = "product.template"

    auren_property_cost_method = fields.Char(compute='_compute_cost_method', string="Costing Method",
                                             )

    def _compute_cost_method(self):
        for val in self:
            if (val.categ_id):
                val.auren_property_cost_method = val.categ_id.property_cost_method
            else:
                val.auren_property_cost_method = ''

    cost_standards_ids = fields.One2many(
        "aurb.cst.cost.standard.item", 'product_id')

    @api.onchange('cost_standards_ids')
    def change_cost(self):

        for item in self:
            price = 0
            for cost in item.cost_standards_ids:
                price += cost.cost
            if (price != 0):
                item.standard_price = price
