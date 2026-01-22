from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastoreMethodPayment(models.Model):
    _name = "aurb.astore.method.payment"
    _description = "AURB aStore Method Payment"

    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    name = fields.Char(index=True, required=True)
    currency_simbol = fields.Char(index=True, required=True)
    journal_id = fields.Many2one(
        "account.journal",
        required=True
    )
    payment_method_id = fields.Many2one(
        "account.payment.method.line",
        required=True
    )
    allowed_payment_method_ids = fields.Many2many(
        "account.payment.method.line",
        compute="_compute_allowed_payment_method_ids"
    )

    method_payment_currency_ids = fields.One2many("aurb.astore.method.payment.currency", "method_payment_id",
                                                  required=True
                                                  )

    @api.depends('journal_id')
    def _compute_allowed_payment_method_ids(self):
        for record in self:
            if record.journal_id:
                record.allowed_payment_method_ids = record.journal_id.inbound_payment_method_line_ids
            else:
                record.allowed_payment_method_ids = False
