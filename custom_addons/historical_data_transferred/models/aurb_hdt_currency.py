from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCurrency(models.Model):
    _name = "aurb.hdt.currency"
    _description = "AURB Currency"
    _rec_name = "name"
    _order = "name desc"

    name = fields.Char(index=True, required=True)
    moneda = fields.Char()
    descripcion = fields.Char()
    descripcion_ab = fields.Char()
    n_decimales = fields.Integer()
    uem = fields.Char()
    triangula = fields.Char()
    dec_linea = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.descripcion != False:
                view_name = record.descripcion
            record.display_name = view_name