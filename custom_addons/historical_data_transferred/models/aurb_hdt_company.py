from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtCompany(models.Model):
    _name = "aurb.hdt.company"
    _description = "AURB Company"
    _rec_name = "name"
    _order = "titulo desc"

    name = fields.Char(index=True, required=True)
    empresa = fields.Char()
    titulo = fields.Char()
    direccion = fields.Char()
    poblacion = fields.Char()
    provincia = fields.Char()
    pais_id = fields.Many2one('aurb.hdt.country','pais_id')
    pais = fields.Char()
    cp = fields.Integer()
    telefono = fields.Char()
    nif = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.titulo != False:
                view_name = record.titulo
            record.display_name = view_name
