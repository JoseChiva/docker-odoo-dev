from odoo import models, fields, api, Command
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import date


class AurbastorePaymentsPos(models.Model):
    _name = "aurb.astore.payments.pos"
    _description = "AURB aStore Payments TPV"

    name = fields.Char(required=True)
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    pos_id = fields.Many2one("aurb.astore.pos", required=True)
    # description = fields.Char(required=True)
    category_id = fields.Many2one(
        "aurb.astore.payments.category.pos", required=True)
    date = fields.Date(required=True)

    type_move = fields.Selection(required=True, selection=[
        ('in', 'In'),
        ('out', 'Out'),
    ], default="out")

    amount = fields.Float(required=True, string="amount_payment_pos")
    posted = fields.Boolean(default=False)

    move_id = fields.Many2one("account.move", string="move_id_payments_pos")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        defaults.setdefault('pos_id', user.pos_id.id)
        defaults.setdefault('date', date.today())
        return defaults

    def action_payment_posted(self):
        for payment in self:
            cid = payment.env.company.id

            amount = payment.amount
            if (payment.type_move == "out"):
                amount = -amount

            date = payment.date
            # account_id = payment.account_id
            pos_id = payment.pos_id.id

            account_id_debit = payment.pos_id.account_id.id
            account_id_credit = payment.category_id.account_id.id
            journal_id = payment.category_id.journal_id.id

            move = payment.env["account.move"].create({
                "company_id": cid,
                "move_type": "entry",
                "journal_id": journal_id,
                "date": date,
                "pos_id": pos_id,
                "type": payment.type_move,
                "line_ids": [
                    Command.create({
                        "name": payment.name,
                        "account_id": account_id_debit,
                        "debit": amount,
                    }),
                    Command.create({
                        "name": payment.name,
                        "account_id": account_id_credit,
                        "credit": amount,
                    }),
                ],
            })

            parameters = self.env['ir.config_parameter'].sudo()
            auto_posted_account_move = parameters.get_param(
                'astore.auto_posted_account_move')
            if (auto_posted_account_move):
                move.state = "posted"

            payment.move_id = move
            payment.posted = True

        return True
