from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class PedretAccountPayment(models.Model):
    _inherit = "account.payment"

    res_partner_invoice = fields.Many2one(
        "res.partner", string="Dirección facturación", compute='_compute_res_partner_invoice', store=True, readonly=False,)

    def _compute_res_partner_invoice(self):
        for payment in self:
            for factura_lin in payment.reconciled_invoice_ids:
                if factura_lin.partner_id:
                    payment.res_partner_invoice = factura_lin.partner_id
