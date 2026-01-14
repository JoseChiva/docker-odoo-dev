from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosAssignment(models.Model):
    _name = "aurb.hdt.pos.assignment"
    _description = "AURB POS assignment"
    _rec_name = "name"

    name = fields.Char()
    usuario = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    tpv = fields.Integer()
    subcta_contado_s_id = fields.Many2one("aurb.hdt.subaccounts")
    subcta_contado_n_id = fields.Many2one("aurb.hdt.subaccounts")
    importe_maximo = fields.Float()
    subcta_caja_id = fields.Many2one("aurb.hdt.subaccounts")
    subcta_pendte_id = fields.Many2one("aurb.hdt.subaccounts")
    concepto_caja = fields.Integer()
    concepto_pendte = fields.Integer()
    concepto_cliente = fields.Integer()
    tipo_contado_1 = fields.Char()
    idioma_1_id = fields.Many2one("aurb.hdt.languages")
    tipo_contado_2 = fields.Char()
    idioma_2_id = fields.Many2one("aurb.hdt.languages")
    tipo_pgo_auxiliar = fields.Char()
    idioma_auxiliar_id = fields.Many2one("aurb.hdt.languages")
    numero_s0401_1 = fields.Integer()
    numero_s0401_2 = fields.Integer()
    tarifa_1 = fields.Char()
    tarifa_2 = fields.Char()
    tarifa_3 = fields.Char()
    tarifa_4 = fields.Char()
    report_presupuesto = fields.Char()
    report_pedido = fields.Char()
    report_albaran = fields.Char()
    report_factura = fields.Char()
    report_tiquet = fields.Char()
    subcta_tiquet_n_id = fields.Many2one("aurb.hdt.subaccounts")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.usuario != False:
                view_name += ' ' + str(record.usuario)
            if record.tpv != False:
                view_name += ' ' + str(record.tpv)
            record.display_name = view_name