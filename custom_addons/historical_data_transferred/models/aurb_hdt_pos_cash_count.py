from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPosCashCount(models.Model):
    _name = "aurb.hdt.pos.cash.count"
    _description = "AURB POS Cash count"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    tpv_id = fields.Many2one("aurb.hdt.pos")
    fecha = fields.Date()
    ar1 = fields.Integer()
    ar2 = fields.Integer()
    ar3 = fields.Integer()
    ar4 = fields.Integer()
    ar5 = fields.Integer()
    ar6 = fields.Integer()
    ar7 = fields.Integer()
    ar8 = fields.Integer()
    ar9 = fields.Integer()
    ar10 = fields.Integer()
    ar11 = fields.Integer()
    ar12 = fields.Integer()
    ar13 = fields.Integer()
    ar14 = fields.Integer()
    ar15 = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.tpv_id.tpv != False:
                view_name += ' ' + str(record.tpv_id.tpv)
            if record.fecha != False:
                view_name += ' ' + str(record.fecha)
            record.display_name = view_name