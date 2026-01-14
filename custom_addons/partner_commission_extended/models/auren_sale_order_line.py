from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class AurenSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commission = fields.Float('% Comisión', default=0)
    manual_commission = fields.Boolean('Comisión manual', default=False)

    @api.onchange('commission')
    def _change_commision(self):
        for line in self:
            if (line.commission != 0):
                line.manual_commission = True
                line.order_id._compute_commission()
