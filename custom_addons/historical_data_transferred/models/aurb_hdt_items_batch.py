from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtItemsBatch(models.Model):
    _name = "aurb.hdt.items.batch"
    _description = "AURB Items Batch"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    codigo_id = fields.Many2one("aurb.hdt.items")

    lote_interno = fields.Char()
    lote_compra = fields.Char()
    almacen_id = fields.Many2one("aurb.hdt.warehouse")

    ubicacion = fields.Char()
    stock_actual = fields.Float()
    stock_bultos = fields.Float()
    stock_reserva = fields.Float()
    stock_reserva_b = fields.Float()
    fecha_cad = fields.Date()
    estado = fields.Char()
    fecha_alta = fields.Date()
    fecha_bloq = fields.Date()

    motivo = fields.Char()
    observacion = fields.Char()
    codigo_prov = fields.Char()
    cantidad_entra = fields.Float()
    subcta_prov = fields.Char()
    cod_mezcla = fields.Char()
    rendimiento = fields.Float()

    precio = fields.Float()
    cantidad_real = fields.Float()
    ejercicio = fields.Integer()
    documento = fields.Integer()
    tipo_doc = fields.Char()
    linea_doc = fields.Integer()
    orden = fields.Integer()

    campo1 = fields.Char()
    campo2 = fields.Char()
    campo3 = fields.Char()
    campo4 = fields.Char()
    campo5 = fields.Char()

    cantidad_bruta = fields.Float()

    presentacion = fields.Char()
    urdido = fields.Char()
    pieza_teje = fields.Char()
    documento_teje = fields.Char()
    stock_reserva_cp = fields.Char()
    stock_reserva_bcp = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.almacen_id.nombre != False:
                view_name += ' ' + record.almacen_id.nombre
            if record.codigo_id.codigo != False:
                view_name += ' ' + record.codigo_id.codigo
            if record.lote_interno != False:
                view_name += ' ' + record.lote_interno
            record.display_name = view_name