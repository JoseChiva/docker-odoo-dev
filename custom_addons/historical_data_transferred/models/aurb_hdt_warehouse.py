from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtWarehouse(models.Model):
    _name = "aurb.hdt.warehouse"
    _description = "AURB Warehouse"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company", string='empresa_id')
    
    empresa = fields.Char()
    almacen = fields.Integer()
    nombre = fields.Char()

    direccion = fields.Char()
    poblacion = fields.Char()
    provincia = fields.Integer()
    pais = fields.Integer()
    cp = fields.Integer()
    telefonos = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.nombre != False:
                view_name += ' ' + record.nombre
            record.display_name = view_name