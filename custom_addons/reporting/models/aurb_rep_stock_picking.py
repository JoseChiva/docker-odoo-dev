from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from .aurb_rep_format_function import get_format_print


class AurbRepStockPicking(models.Model):
    _inherit = "stock.picking"

    valorado = fields.Boolean(
        default=True, string="Valorado")

    def do_print_picking(self):
        for record in self:
            partner_id = record.partner_id.id
            report = get_format_print(
                partner_id, self)
            if (report != False):
                return report.report_action(self)
            else:
                raise ValidationError(
                    "No se encontrado un modelo de impresión configurado")
        # return self.env.ref('reporting.report_event_registration_badge_stock_picking').report_action(self)
