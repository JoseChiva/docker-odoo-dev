from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmCostStandard(models.Model):
    _name = "aurb.cm.cost.standard"
    _description = "Aurb Cost Standard"

    name = fields.Char(index=True)
