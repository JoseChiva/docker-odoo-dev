from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersAddress(models.Model):
    _name = "aurb.hdt.partners.address"
    _description = "AURB Address Cards"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.partners")
    orden = fields.Integer()
    nombre_comercial = fields.Char()
    nombre_comercial2 = fields.Char()
    dni_nif = fields.Char()
    direccion = fields.Char()
    direccion2 = fields.Char()
    pais = fields.Integer()
    provincia = fields.Integer()
    codigo_postal = fields.Integer()
    codigo_postal2 = fields.Char()
    poblacion = fields.Char()
    poblacion2 = fields.Char()
    telefonos = fields.Char()
    idioma = fields.Integer()
    tipus = fields.Char()
    contacte = fields.Char()
    
    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            if record.orden != False:
                view_name += ' ' + str(record.orden)
            record.display_name = view_name