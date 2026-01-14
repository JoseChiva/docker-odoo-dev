from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtBankEntity(models.Model):
    _name = "aurb.hdt.bank.entity"
    _description = "AURB Bank Entity"
    _rec_name = "name"
    _order = "ccc1 desc"

    name = fields.Char(index=True, required=True)
    ccc1 = fields.Char()
    nombre = fields.Char()
    swift = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.nombre != False:
                view_name = record.nombre
            if record.ccc1 != False:
                view_name += ' ' + record.ccc1
            record.display_name = view_name
