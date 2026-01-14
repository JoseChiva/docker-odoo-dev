from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOutcomingPaymentsTpv(models.Model):
    _name = "aurb.hdt.outcoming.payments.tpv"
    _description = "AURB outcoming Payments TPV"
    _rec_name = "name"
    _order = "empresa_id,tpv desc"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")

    tpv = fields.Integer()
    concepto1 = fields.Char()
    concepto2 = fields.Char()

    fecha = fields.Date()
    importe = fields.Float()

    asiento = fields.Integer()
    tipo_doc = fields.Selection(
        selection=[
            ('PV', "Pedido venta"),
            ('PP', "Presupuesto"),
            ('PC', "Pedido compra"),
            ('EF', "Entrada fabricación"),
            ('SV', "Albaranes de venta"),
            ('NF', "No facturable venta"),
            ('SF', "Salida fabricación"),
            ('NC', "No facturable compra"),
            ('EC', "Albaranes de Compra"),
        ]
    )

    alternativo = fields.Integer()
    codigo_pago = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.tpv != False:
                view_name += ' ' + str(record.tpv)
            if record.tipo_doc != False:
                view_name += ' ' + record.tipo_doc
            if record.concepto1 != False:
                view_name += ' ' + record.concepto1
            record.display_name = view_name