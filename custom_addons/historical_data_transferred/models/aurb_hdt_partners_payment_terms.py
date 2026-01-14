from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersPaymentTerms(models.Model):
    _name = "aurb.hdt.partners.payment.terms"
    _description = "AURB Partners Payment Terms"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.partners")
    linea_producto = fields.Integer()
    clv_sub = fields.Integer()
    tipo_forma_pago = fields.Char()
    numero_recibos = fields.Integer()
    primer_intervalo = fields.Integer()
    otros_intervalos = fields.Integer()
    dia_fijo_pago_1 = fields.Integer()
    dia_fijo_pago_2 = fields.Integer()
    entidad_bancaria = fields.Integer()
    numero_cuenta = fields.Char()
    ccc1 = fields.Char()
    ccc2 = fields.Char()
   # ccc1_id = fields.Many2one("aurb.hdt.bank.office")
   # ccc2_id = fields.Many2one("aurb.hdt.bank.entity")
    dc = fields.Char()
    subcta_banco_remes = fields.Char()
    swift = fields.Char()
   # swift_id = fields.Many2one("aurb.hdt.bank.entity")
    iban = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            record.display_name = view_name