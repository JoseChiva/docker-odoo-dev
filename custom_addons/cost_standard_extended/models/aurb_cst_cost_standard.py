from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCstCostStandard(models.Model):
    _name = "aurb.cst.cost.standard"
    _description = "Aurb Cost Standard"

    name = fields.Char(index=True)

    cost = fields.Float(string="Cost")
