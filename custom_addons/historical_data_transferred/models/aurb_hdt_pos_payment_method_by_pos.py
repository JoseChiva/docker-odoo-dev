from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosPaymentMethodByPos(models.Model):
    _name = "aurb.hdt.pos.payment.method.by.pos"
    _description = "AURB POS payment method by pos"
    _rec_name = "name"
    _order = "empresa_id asc, tpv asc, codigo_pago_id asc"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")
    tpv = fields.Integer()
    codigo_pago_id = fields.Many2one("aurb.hdt.pos.payment.method")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.tpv != False:
                view_name += ' ' + str(record.tpv)
            if record.codigo_pago_id.descripcion != False:
                view_name += ' ' + record.codigo_pago_id.descripcion
            record.display_name = view_name