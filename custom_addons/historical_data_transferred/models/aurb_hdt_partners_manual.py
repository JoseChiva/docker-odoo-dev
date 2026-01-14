from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersManual(models.Model):
    _name = "aurb.hdt.partners.manual"
    _description = "AURB Partners Manual"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio = fields.Integer()
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    documento = fields.Integer()
    tipo_doc = fields.Char()
    subcta_id = fields.Many2one("aurb.hdt.partners")
    asiento = fields.Integer()
    asiento_id = fields.Many2one('aurb.hdt.accounting.entries', string='asiento_id')
    orden = fields.Integer()
    titulo = fields.Char()
    dni_nif = fields.Char()
    direccion = fields.Char()
    pais = fields.Integer()
    provincia = fields.Integer()
    codigo_postal = fields.Integer()
    poblacion = fields.Char()
    idioma = fields.Integer()
    telefonos = fields.Char()
    observacion = fields.Char()
    claveman = fields.Char()
    orden_origen = fields.Integer()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.ejercicio != False:
                view_name += ' ' + str(record.ejercicio)
            if record.titulo != False:
                view_name += ' ' + record.titulo
            record.display_name = view_name