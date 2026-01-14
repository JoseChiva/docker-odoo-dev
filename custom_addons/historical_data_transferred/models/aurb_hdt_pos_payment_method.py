from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosPaymentMethod(models.Model):
    _name = "aurb.hdt.pos.payment.method"
    _description = "AURB POS payment method"
    _rec_name = "name"
    _order = "codigo_pago desc"

    name = fields.Char(index=True, required=True)
    codigo_pago = fields.Integer()
    descripcion = fields.Char()
    tipo = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.descripcion != False:
                view_name = record.descripcion
            record.display_name = view_name