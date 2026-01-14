from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersCards(models.Model):
    _name = "aurb.hdt.partners.cards"
    _description = "AURB Partners Cards"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.partners")
    num_tarjeta = fields.Char()
    tipo_doc = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            if record.num_tarjeta != False:
                view_name += ' ' + record.num_tarjeta
            record.display_name = view_name