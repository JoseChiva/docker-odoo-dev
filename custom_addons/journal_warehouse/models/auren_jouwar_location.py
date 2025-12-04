from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurenJouWarAccountMove(models.Model):
    _inherit = "stock.location"

    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        domain="[('type', '=', 'sale')]"
    )
