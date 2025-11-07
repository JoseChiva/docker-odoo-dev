from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from .aurb_rep_format_function import get_format_print


class AurbRepSaleOrder(models.Model):
    _inherit = "sale.order"

    valorado = fields.Boolean(
        default=True, string="Valorado")

    def action_print_default(self):
        for record in self:
            partner_id = record.partner_id.id
            report = get_format_print(
                partner_id, self)
            if (report != False):
                return report.report_action(self)
            else:
                raise ValidationError(
                    "No se encontrado un modelo de impresión configurado")

        # return self.env.ref('reporting.report_event_registration_badge_sale_order').report_action(self)
