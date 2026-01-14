from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtItemsBatchIncident(models.Model):
    _name = "aurb.hdt.items.batch.incident"
    _description = "AURB Items Batch Incident"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    codigo_id = fields.Many2one("aurb.hdt.items")
    lote_interno_id = fields.Many2one("aurb.hdt.items.batch")

    lote_compra = fields.Char()
    incidencia = fields.Char()

    fecha_entrada = fields.Date()
    hora_entrada = fields.Char()
    usuario_entrada = fields.Char()

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
            if record.incidencia != False:
                view_name += ' ' + record.incidencia
            record.display_name = view_name