from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class AurbPedretPurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    res_partner_id = fields.Many2one("res.partner", string="Obra")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            if record.res_partner_id:
                record.display_name = f"{record.name} - {record.res_partner_id.name}"
            else:
                record.display_name = f"{record.name}"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        # Búsqueda extendida que incluye nombre, proveedor, estado, etc.
        args = args or []
        domain = []
        if name:
            domain = ['|',
                      ('name', operator, name),
                      ('res_partner_id.name', operator, name),
                      ]
        return self.search(domain + args, limit=limit).name_get()
