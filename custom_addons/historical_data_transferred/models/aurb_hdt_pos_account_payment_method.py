from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosAccountPaymentMethod(models.Model):
    _name = "aurb.hdt.pos.account.payment.method"
    _description = "AURB POS account payment method"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    codigo_pago_id = fields.Many2one("aurb.hdt.pos.payment.method")
    subcta_id = fields.Many2one("aurb.hdt.subaccounts")
    concepto = fields.Integer()
    diario = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.codigo_pago_id.descripcion != False:
                view_name += ' ' + str(record.codigo_pago_id.descripcion)
            record.display_name = view_name