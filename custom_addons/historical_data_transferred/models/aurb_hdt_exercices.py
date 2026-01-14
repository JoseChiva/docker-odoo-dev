from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtExercices(models.Model):
    _name = "aurb.hdt.exercices"
    _description = "AURB Exercices"
    _rec_name = "name"

    name = fields.Char()
    empresa = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company",string='empresa_id')
    ejercicio = fields.Integer()
    fecinicio = fields.Date()
    fecfinal = fields.Date()
    estado = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.ejercicio != False:
                view_name += ' ' + str(record.ejercicio)
            record.display_name = view_name