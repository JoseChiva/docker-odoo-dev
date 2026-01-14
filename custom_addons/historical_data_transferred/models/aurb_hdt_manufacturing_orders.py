from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtManufacturingOrders(models.Model):
    _name = "aurb.hdt.manufacturing.orders"
    _description = "AURB Manufacturing Orders"
    _rec_name = "name"
    _order = "empresa_id,ejercicio_id,almacen_id,documento_sf desc"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    fecha_sf = fields.Date()
    fecha_ef = fields.Date()
    documento_sf = fields.Integer()
    documento_ef = fields.Integer()

    lote = fields.Char()
    subcta_c = fields.Char()
    subcta_s = fields.Char()
    pedido = fields.Integer()
    linea_pedido = fields.Integer()

    articulo = fields.Char()
    cantidad_sf = fields.Float()
    cantidad_ef = fields.Float()
    observaciones = fields.Char()
    n_traspaso = fields.Integer()
    estado = fields.Char()
    of_original = fields.Integer()

    lines_ids = fields.One2many(
        "aurb.hdt.manufacturing.orders.lines", "documento_id")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.documento_sf != False:
                view_name = str(record.documento_sf)
            record.display_name = view_name