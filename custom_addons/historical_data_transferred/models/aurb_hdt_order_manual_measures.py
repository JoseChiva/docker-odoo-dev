from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOrderManualMeasures(models.Model):
    _name = "aurb.hdt.order.manual.measures"
    _description = "AURB Order Medidas manuales"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")

    ejercicio = fields.Integer()

    almacen_id = fields.Many2one("aurb.hdt.warehouse")

    documento_id = fields.Many2one("aurb.hdt.document", required=True)

    tipo_movimiento = fields.Selection(
        selection=[
            ('PV', "Pedido venta"),
            ('PP ', "Presupuesto"),
            ('PC', "Pedido compra"),
            ('EF', "Entrada fabricación"),
            ('SV', "Albaranes de venta"),
            ('NF', "No facturable venta"),
            ('SF', "Salida fabricación"),
            ('NC', "No facturable compra"),
            ('EC', "Albaranes de Compra"),
        ]
    )

    linea_documento = fields.Integer()
    linea_documento_id = fields.Many2one(
        "aurb.hdt.document.lines", required=True, string="documento_id")

    linea_medida = fields.Integer()
    bultos = fields.Float()
    cantidad = fields.Float()
    largo = fields.Float()
    ancho = fields.Float()
    grueso = fields.Float()
    procede = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.tipo_doc != False:
                view_name = record.tipo_doc
            if record.documento_id != False:
                view_name += ' ' + str(record.documento_id)
            if record.largo != False:
                view_name += ' ' + str(record.largo)
            if record.ancho != False:
                view_name += ' ' + str(record.ancho)
            if record.grueso != False:
                view_name += ' ' + str(record.grueso)
            record.display_name = view_name