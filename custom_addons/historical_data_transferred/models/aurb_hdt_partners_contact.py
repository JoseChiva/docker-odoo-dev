from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersContact(models.Model):
    _name = "aurb.hdt.partners.contact"
    _description = "AURB Partners Contact"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.partners")
    contacto = fields.Char()
    persona_contacto = fields.Char()
    telefono = fields.Char()
    fax = fields.Char()
    observaciones = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            if record.persona_contacto != False:
                view_name += ' ' + record.persona_contacto
            record.display_name = view_name