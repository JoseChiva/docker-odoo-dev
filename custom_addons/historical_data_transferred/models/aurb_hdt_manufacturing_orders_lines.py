from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtStockTransferLines(models.Model):
    _name = "aurb.hdt.manufacturing.orders.lines"
    _description = "AURB Manufacturing Orders Lines"
    _rec_name = "name"
    _order = "empresa_id,ejercicio_id,documento_id desc"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    documento_id = fields.Many2one("aurb.hdt.manufacturing.orders")

    fecha_documento = fields.Date()
    linea_documento = fields.Integer()
    tipo_movimiento = fields.Selection(
        selection=[
            ('RC', "Recuento"),
            ('EF', "Entrada Fabricación"),
            ('SF', "Salida Fabricación"),
            ('EI', "Existencia Inicial"),
            ('SV', "Albaranes de venta"),
            ('NF', "No facturable venta"),
            ('NC', "No facturable compra"),
            ('EC', "Albaranes de Compra"),
            ('CO', "Contado")
        ]
    )    
    
    subcta_c = fields.Char()
    subcta_s = fields.Char()
    pedido = fields.Integer()
    fase = fields.Integer()
    codigo = fields.Integer()

    articulo = fields.Char()
    clv_art = fields.Char()
    cantidad = fields.Float()
    bultos = fields.Float()
    precio = fields.Float()
    precio_coste = fields.Float()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    cambio = fields.Float()
    cambio_euro = fields.Float()

    impresa = fields.Integer()
    fecha_entrada = fields.Date()
    usuario_entrada = fields.Char()
    hora_entrada = fields.Char()
    fecha_modifi = fields.Date()
    usuario_modifi = fields.Char()
    hora_modifi = fields.Char()

    acumula = fields.Integer()
    base = fields.Float()
    lote_interno = fields.Char()
    campo1 = fields.Char()
    campo2 = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.tipo_movimiento != False:
                view_name = record.tipo_movimiento
            if record.documento_id.documento_sf != False:
                view_name += ' ' + str(record.documento_id.documento_sf)
            if record.linea_documento != False:
                view_name += ' ' + str(record.linea_documento)
            record.display_name = view_name