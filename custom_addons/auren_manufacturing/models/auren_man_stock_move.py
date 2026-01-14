from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

# create attachment and download
import base64


class AurenManStockMove(models.Model):
    _inherit = "stock.move"

    unit_ua = fields.Float(
        string="Unidades", compute="_compute_time", store=True)
    var1 = fields.Float(string="var1", compute="_compute_time", store=True)
    var2 = fields.Float(string="var2", compute="_compute_time", store=True)
    var3 = fields.Float(string="var3", compute="_compute_time", store=True)
    formula = fields.Char(
        string="Fórmula", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", compute="_compute_time", store=True
    )
    qty_inventory = fields.Float(
        string="Quantity Inventory", default=1, digits=(12, 5))
    conversion_factor = fields.Float(
        string="conversion_factor", default=1, digits=(12, 8))
    unit__factor = fields.Float(
        string="unit__factor", default=1, digits=(12, 8))

    @api.depends('bom_line_id')
    def _compute_time(self):
        for comp in self:
            if (comp.bom_line_id != False):
                comp.unit_ua = comp.bom_line_id.unit_ua
                comp.var1 = comp.bom_line_id.var1
                comp.var2 = comp.bom_line_id.var2
                comp.var3 = comp.bom_line_id.var3
                comp.formula = comp.bom_line_id.formula
