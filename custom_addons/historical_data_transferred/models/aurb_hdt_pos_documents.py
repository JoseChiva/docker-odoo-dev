from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosDocuments(models.Model):
    _name = "aurb.hdt.pos.documents"
    _description = "AURB POS documents"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    documento = fields.Integer()
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
            ('FV', "Facturas de Venta"),
        ]
    )
    orden_vto = fields.Integer()
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    fecha = fields.Date()
    codigo_pago = fields.Integer()
    banco = fields.Char()
    n_cuenta = fields.Char()
    numero_tt = fields.Char()
    importe = fields.Float()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    cambio = fields.Float()
    cambio_euro = fields.Float()
    tipo = fields.Integer()
    tpv_id = fields.Many2one("aurb.hdt.pos")
    clave = fields.Char()
    
    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.tpv_id.tpv != False:
                view_name += ' ' + str(record.tpv_id.tpv)
            if record.tipo_doc != False:
                view_name += ' ' + record.tipo_doc
            if record.documento != False:
                view_name += ' ' + str(record.documento)
            record.display_name = view_name