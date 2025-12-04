from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastoreMovePos(models.Model):
    _name = "aurb.astore.move.pos"
    _description = "AURB aStore Movimientos TPV"

    pos_id = fields.Many2one("aurb.astore.pos")
    account_move_id = fields.Many2one("account.move")
    date = fields.Date()

    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    active = fields.Boolean(default=True)
    amount = fields.Float(string="amount_move")

    closed = fields.Boolean(default=False)

    close_pos_id = fields.Many2one("aurb.astore.close.pos")

    type = fields.Selection(required=True, selection=[
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'Miscellaneous'),
    ])
