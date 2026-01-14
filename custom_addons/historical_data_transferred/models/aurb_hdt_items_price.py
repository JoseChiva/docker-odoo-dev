from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtItemsPrice(models.Model):
    _name = "aurb.hdt.items.price"
    _description = "AURB Items price"
    _rec_name = "name"
    '''
    _inherits = {
        'aurb.hdt.items': 'codigo_id'
    }
    '''
    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    codigo_id = fields.Many2one("aurb.hdt.items")
    clv_art = fields.Integer()

    precio_std_1 = fields.Float()
    fecha_std_1 = fields.Date()
    precio_std_2 = fields.Float()
    precio_std_3 = fields.Float()
    precio_std_4 = fields.Float()

    precio_u_entrada = fields.Float()
    moneda_id = fields.Many2one("aurb.hdt.currency")
    cambio = fields.Float()
    cambio_euro = fields.Float()
    tipo_iva = fields.Integer()
    variante = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.codigo_id.codigo != False:
                view_name += ' ' + record.codigo_id.codigo
            if record.variante != False:
                view_name += ' ' + record.variante
            record.display_name = view_name
