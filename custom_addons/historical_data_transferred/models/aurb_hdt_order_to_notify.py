from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOrderToNotify(models.Model):
    _name = "aurb.hdt.order.to.notify"
    _description = "AURB Order to notify"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    doc = fields.Integer()
    observacion = fields.Char()
    faviso = fields.Date()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.ejercicio_id.ejercicio != False:
                view_name += ' ' + str(record.ejercicio_id.ejercicio)
            if record.doc != False:
                view_name += ' ' + str(record.doc)
            record.display_name = view_name