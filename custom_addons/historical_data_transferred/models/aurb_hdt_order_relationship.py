from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOrderRelationship(models.Model):
    _name = "aurb.hdt.order.relationship"
    _description = "AURB Order relationship"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    doc = fields.Integer()
    fdoc = fields.Date()
    su = fields.Char()
    tit = fields.Char()
    odlin = fields.Integer()
    art = fields.Char()
    desm = fields.Char()
    supro = fields.Char()
    cant = fields.Float()
    preu = fields.Float()
    dto_1 = fields.Float()
    dto_2 = fields.Float()
    dto_3 = fields.Float()
    empresa1_id = fields.Many2one("aurb.hdt.company")
    ejercicio1_id = fields.Many2one("aurb.hdt.exercices")
    doc1 = fields.Integer()
    odlin1 = fields.Integer()
    titemp = fields.Char()
    usu = fields.Char()
    fservicio = fields.Date()
    ports = fields.Float()
    cport = fields.Char()
    cconf = fields.Char()
    cimp = fields.Char()
    agencia = fields.Integer()
    comentario = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.doc != False:
                view_name += ' ' + str(record.doc)
            if record.empresa1_id.titulo != False:
                view_name += ' ' + record.empresa1_id.titulo
            if record.doc1 != False:
                view_name += ' ' + str(record.doc1)
            record.display_name = view_name