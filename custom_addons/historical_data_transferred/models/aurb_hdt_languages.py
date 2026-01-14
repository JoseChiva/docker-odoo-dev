from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtLanguages(models.Model):
    _name = "aurb.hdt.languages"
    _description = "AURB Languages"
    _rec_name = "name"

    name = fields.Char()
    idioma = fields.Integer()
    nombre = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.nombre != False:
                view_name = record.nombre
            record.display_name = view_name