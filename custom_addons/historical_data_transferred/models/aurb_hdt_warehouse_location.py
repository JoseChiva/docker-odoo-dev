from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtWarehouseCurrency(models.Model):
    _name = "aurb.hdt.warehouse.location"
    _description = "AURB Warehouse Location"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")

    ubicado = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.almacen_id.nombre != False:
                view_name += ' ' + record.almacen_id.nombre
            if record.ubicado != False:
                view_name += ' ' + str(record.ubicado)
            record.display_name = view_name