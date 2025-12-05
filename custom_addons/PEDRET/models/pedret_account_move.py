from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class PedretAccountMove(models.Model):
    _inherit = "account.move"

    num_contract = fields.Char()
