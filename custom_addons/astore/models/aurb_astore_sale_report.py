
from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbaStoreSaleReport(models.Model):
    _inherit = "sale.report"

    pos_id = fields.Many2one("aurb.astore.pos", string="POS", readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['pos_id'] = f"""s.pos_id"""
        return res
