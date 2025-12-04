from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastoreAccountPaymentMethodPayment(models.TransientModel):
    _name = "aurb.astore.account.payment.method.payment"
    _description = "AURB aStore Account Payment Method Payment"
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    account_payment_method_bill_id = fields.Many2one("account.payment.register",
                                                     ondelete='cascade'
                                                     )
    account_payment_method_coin_id = fields.Many2one("account.payment.register",
                                                     ondelete='cascade'
                                                     )

    method_payment_currency_id = fields.Many2one("aurb.astore.method.payment.currency",
                                                 ondelete='cascade'
                                                 )
    number = fields.Float()
    order = fields.Float()
