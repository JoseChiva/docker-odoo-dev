from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCurrencySubaccount(models.Model):
    _name = "aurb.hdt.currency.subaccount"
    _description = "AURB Currency Subaccount"
    _rec_name = "name"
    _order = "name desc"

    name = fields.Char(index=True, required=True)
    moneda = fields.Integer()
    moneda_ref = fields.Char()
    moneda_id = fields.Many2one("aurb.hdt.currency",string= 'moneda_id',)
    base = fields.Integer()
    dif_pos = fields.Char()
    dif_neg = fields.Char()
    subcta_comp = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.moneda_ref != False:
                view_name = record.moneda_ref
            record.display_name = view_name