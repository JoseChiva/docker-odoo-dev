from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastoreMethodPaymentCurrency(models.Model):
    _name = "aurb.astore.method.payment.currency"
    _description = "AURB aStore Method Payment Currency"

    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    name = fields.Char(index=True, required=True)
    value = fields.Float(index=True, required=True)
    order = fields.Integer()
    method_payment_id = fields.Many2one(
        "aurb.astore.method.payment",
        required=True, ondelete='cascade'
    )

    type = fields.Selection(required=True, selection=[
        ('coin', 'Coin'),
        ('bill', 'Bill'),
    ])

#   @api.depends('code')
#     def _compute_display_name(self):
#         for incoterm in self:
#             incoterm.display_name = '%s%s' % (incoterm.code and '[%s] ' % incoterm.code or '', incoterm.name)

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name+' '+record.method_payment_id.currency_simbol
            record.display_name = view_name
