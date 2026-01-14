from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtDeliveryZone(models.Model):
    _name = "aurb.hdt.delivery.zone"
    _description = "AURB Delivery Zone"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    zona_entrega = fields.Char()
    descripcion = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.zona_entrega != False:
                view_name += ' ' + record.zona_entrega
            record.display_name = view_name