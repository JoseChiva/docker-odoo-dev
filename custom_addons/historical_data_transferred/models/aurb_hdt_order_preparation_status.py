from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOrderPreparationStatus(models.Model):
    _name = "aurb.hdt.order.preparation.status"
    _description = "AURB Order preparation status"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    tipo_movimiento = fields.Char()
    pedido = fields.Integer()
    od_linea = fields.Integer()
    tipo = fields.Char()
    usuario_entrada = fields.Char()
    fecha_entrada = fields.Date()
    hora_entrada = fields.Char()
    usuario_preparacio = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.ejercicio_id.ejercicio != False:
                view_name += ' ' + str(record.ejercicio_id.ejercicio)
            if record.pedido != False:
                view_name += ' ' + str(record.pedido)
            record.display_name = view_name