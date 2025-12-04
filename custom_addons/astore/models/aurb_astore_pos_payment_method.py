from odoo import models, fields, api, tools, Command
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastorePosPaymentMethod(models.Model):
    _name = "aurb.astore.pos.payment.method"
    _description = "AURB aStore Pos Payment Method"
    _sql_constraints = [
        ('pk_astore_pos_payment_method', 'unique(pos_id,payment_method_id)',
         'Este metodo de pago ya existe'),
    ]
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    name = fields.Char()

    pos_id = fields.Many2one(
        "aurb.astore.pos",  required=True, index=True)

    payment_method_id = fields.Many2one(
        "aurb.astore.method.payment",  required=True, index=True)

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.payment_method_id.name
            record.display_name = view_name
