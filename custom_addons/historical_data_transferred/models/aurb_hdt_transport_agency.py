from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtTransportAgency(models.Model):
    _name = "aurb.hdt.transport.agency"
    _description = "AURB Transport Agency"
    _rec_name = "name"

    name = fields.Char()
    codigo = fields.Integer()
    nombre = fields.Char()
    direccion = fields.Char()
    poblacion = fields.Char()
    provincia = fields.Integer()
    pais = fields.Integer()
    cp = fields.Integer()
    telefono = fields.Char()
    fax = fields.Char()
    p_contacto = fields.Char()
    observacones = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.nombre != False:
                view_name = record.nombre
            record.display_name = view_name