from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtVehicle(models.Model):
    _name = "aurb.hdt.vehicle"
    _description = "AURB Vehicle"
    _rec_name = "name"
    _order = "codigo desc"

    name = fields.Char(index=True, required=True)
    codigo = fields.Integer()
    marca = fields.Char()
    matricula = fields.Char()
    chofer = fields.Char()
    fecha_alta = fields.Date()
    fecha_baja = fields.Date()
    km_inicio = fields.Integer()
    fecha_ult_itv = fields.Date()
    fecha_prox_itv = fields.Date()
    fecha_ult_matp = fields.Date()
    fecha_prox_matp = fields.Date()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.marca != False:
                view_name = record.marca
            if record.matricula != False:
                view_name += ' - ' + record.matricula
            record.display_name = view_name