from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtStockTransferLines(models.Model):
    _name = "aurb.hdt.stock.transfer.lines"
    _description = "AURB Stock Transfer Lines"
    _rec_name = "name"
    _order = "empresa_id,tipo_movimiento,documento_id desc"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")

    tipo_movimiento = fields.Selection(
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
    documento_id = fields.Many2one("aurb.hdt.stock.transfer")
    linea_trs = fields.Integer()
    clv_trs = fields.Integer()
    articulo = fields.Char()
    clv_art = fields.Integer()
    cantidad = fields.Float()
    bultos = fields.Float()
    precio_o = fields.Float()
    precio_d = fields.Float()
    total_linea_o = fields.Float()
    total_linea_o_base = fields.Float()
    total_linea_o_euro = fields.Float()
    total_linea_d = fields.Float()
    total_linea_d_base = fields.Float()
    total_linea_d_euro = fields.Float()

    moneda_o_id = fields.Many2one("aurb.hdt.currency")
    moneda_d_id = fields.Many2one("aurb.hdt.currency")

    cambio_o = fields.Float()
    cambio_o_euro = fields.Float()
    cambio_d = fields.Float()
    cambio_d_euro = fields.Float()

    almacen_o_id = fields.Many2one("aurb.hdt.warehouse")
    almacen_d_id = fields.Many2one("aurb.hdt.warehouse")
    fecha_documento = fields.Date()

    triangulado_o = fields.Char()
    triangulado_d = fields.Char()
    lote_interno = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.tipo_doc != False:
                view_name = record.tipo_doc
            if record.documento != False:
                view_name += ' ' + str(record.documento)
            if record.linea_trs != False:
                view_name += ' ' + str(record.linea_trs)
            record.display_name = view_name