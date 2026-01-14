from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtItemsBatchPiece(models.Model):
    _name = "aurb.hdt.items.batch.piece"
    _description = "AURB Items Batch Piece"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    codigo_id = fields.Many2one("aurb.hdt.items")
    npieza = fields.Char()
    lote_interno_id = fields.Many2one("aurb.hdt.items.batch")

    ubicacion = fields.Char()
    calidad = fields.Char()
    anchura = fields.Char()
    cantidad = fields.Float()
    cantidad_s = fields.Float()
    tara_desc = fields.Char()
    tara_m = fields.Float()

    fecha_fabrica = fields.Date()
    hora_fabrica = fields.Char()
    repasador = fields.Char()
    tabla_repaso = fields.Char()
    bonificacion = fields.Float()
    motivo_boni = fields.Char()
    coste_m = fields.Float()

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
            if record.lote_interno_id.lote_interno != False:
                view_name += ' ' + record.lote_interno_id.lote_interno
            record.display_name = view_name