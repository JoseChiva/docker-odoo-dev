from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosCumulative(models.Model):
    _name = "aurb.hdt.pos.cumulative"
    _description = "AURB POS cumulative"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    fecha = fields.Date()
    cambio = fields.Float()
    recaudacion = fields.Float()
    efectivo = fields.Float()
    ingreso = fields.Float()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    cambio_mon = fields.Float()
    cambio_euro = fields.Float()
    tpv_id = fields.Many2one("aurb.hdt.pos")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.fecha != False:
                view_name += ' ' + str(record.fecha)
            if record.tpv_id.tpv != False:
                view_name += ' ' + str(record.tpv_id.tpv)
            record.display_name = view_name