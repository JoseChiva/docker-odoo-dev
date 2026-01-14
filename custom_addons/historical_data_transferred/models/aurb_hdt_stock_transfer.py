from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtStockTransfer(models.Model):
    _name = "aurb.hdt.stock.transfer"
    _description = "AURB Stock Transfer"
    _rec_name = "name"
    _order = "empresa_id,almacen_o_id,documento desc"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_o_id = fields.Many2one("aurb.hdt.warehouse")
    almacen_d_id = fields.Many2one("aurb.hdt.warehouse")

    n_produccion = fields.Integer()
    documento = fields.Integer()
    fecha_documento = fields.Date()

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
    situacion = fields.Integer()
    fecha_entrada = fields.Date()
    usuario_entrada = fields.Char()
    hora_entrada = fields.Char()
    fecha_modifi = fields.Date()
    usuario_modifi = fields.Char()
    hora_modifi = fields.Char()
    asiento = fields.Integer()

    lines_ids = fields.One2many(
        "aurb.hdt.stock.transfer.lines", "documento_id")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.tipo_doc != False:
                view_name = record.tipo_doc
            if record.documento != False:
                view_name += ' ' + str(record.documento)
            record.display_name = view_name