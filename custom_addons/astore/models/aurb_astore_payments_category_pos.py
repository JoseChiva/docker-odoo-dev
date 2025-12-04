from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastorePaymentsCategoryPos(models.Model):
    _name = "aurb.astore.payments.category.pos"
    _description = "AURB aStore Payments Category TPV"

    name = fields.Char(index=True, required=True)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    account_id = fields.Many2one(
        "account.account", string="account_cat", requerid=True)

    journal_id = fields.Many2one(
        "account.journal",
        required=True
    )
