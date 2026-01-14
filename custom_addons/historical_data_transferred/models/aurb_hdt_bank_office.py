from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtBankEntity(models.Model):
    _name = "aurb.hdt.bank.office"
    _description = "AURB Bank Office"
    _rec_name = "name"
    _order = "ccc1_id asc, ccc2 asc"

    name = fields.Char(index=True, required=True)
    ccc1 = fields.Char()
    ccc1_id = fields.Many2one("aurb.hdt.bank.entity",string = "ccc1_Nombre")
    ccc2 = fields.Char()
    nombre = fields.Char()
    direccion = fields.Char()
    poblacion = fields.Char()
    provincia = fields.Integer()
    pais = fields.Integer()
    cp = fields.Integer()
    telefono = fields.Char()
    fax = fields.Char()
    p_contacto = fields.Char()
    # swift_id = fields.Many2one("aurb.hdt.bank.entity")
    swift = fields.Char()
    iban = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.nombre != False:
                view_name = record.nombre
            if record.ccc1_id.ccc1 != False:
                view_name += ' ' + record.ccc1_id.ccc1
            if record.ccc2 != False:
                view_name += " " + record.ccc2
            record.display_name = view_name