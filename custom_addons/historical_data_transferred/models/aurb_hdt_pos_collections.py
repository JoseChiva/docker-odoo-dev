from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosCollections(models.Model):
    _name = "aurb.hdt.pos.collections"
    _description = "AURB POS collections"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
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
    subcta_id = fields.Many2one("aurb.hdt.subaccounts")
    fecha = fields.Date()
    importe = fields.Float()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    cambio = fields.Float()
    cambio_euro = fields.Float()
    asiento = fields.Integer()
    orden = fields.Integer()
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