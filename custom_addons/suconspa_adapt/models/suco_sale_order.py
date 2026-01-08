from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class SucoSaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        # Call super to preserve existing behavior (sets invoice/shipping by default)
        try:
            super(SucoSaleOrder, self)._onchange_partner_id()
        except Exception:
            # If base method is not present or raises, ignore and continue
            pass
        for order in self:
            if order.partner_id:
                # Force invoice and shipping addresses to be the same as the main partner
                # This ensures that even if the company has child contacts with "Invoice Address"
                # enabled, the main company contact is always used
                order.partner_invoice_id = order.partner_id
                order.partner_shipping_id = order.partner_id

    @api.onchange('partner_invoice_id')
    def _onchange_partner_invoice_id(self):
        # Keep shipping in sync when invoice address is manually changed
        for order in self:
            if order.partner_invoice_id:
                order.partner_shipping_id = order.partner_invoice_id
