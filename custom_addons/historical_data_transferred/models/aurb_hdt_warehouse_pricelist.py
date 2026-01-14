from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtWarehousePriceList(models.Model):
    _name = "aurb.hdt.warehouse.pricelist"
    _description = "AURB Warehouse pricelist"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")

    tarifa = fields.Char()
    tipo = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.almacen_id.nombre != False:
                view_name += ' ' + record.almacen_id.nombre
            if record.tarifa != False:
                view_name += ' ' + str(record.tarifa)
            record.display_name = view_name