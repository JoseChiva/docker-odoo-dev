from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastoreAccountPaymentMethodPayment(models.Model):
    _name = "aurb.astore.close.pos.method.payment"
    _description = "AURB aStore Close Pos Method Payment"
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    account_payment_method_bill_id = fields.Many2one("aurb.astore.close.pos",
                                                     ondelete='cascade'
                                                     )
    account_payment_method_coin_id = fields.Many2one("aurb.astore.close.pos",
                                                     ondelete='cascade'
                                                     )

    method_payment_currency_id = fields.Many2one("aurb.astore.method.payment.currency",
                                                 ondelete='cascade'
                                                 )
    number = fields.Float()
    order = fields.Float()
