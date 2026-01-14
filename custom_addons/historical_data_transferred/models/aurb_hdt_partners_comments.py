from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersComments(models.Model):
    _name = "aurb.hdt.partners.comments"
    _description = "AURB Partners Comments"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.partners")
    tipo_obs = fields.Integer()
    numero_obs = fields.Integer()
    observacion = fields.Char()
    usuarientrada = fields.Char()
    dataalta = fields.Date()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            if record.numero_obs != False:
                view_name += ' ' + str(record.numero_obs)
            record.display_name = view_name