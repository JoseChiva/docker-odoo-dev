from odoo import models, fields

class GITypePrice(models.Model):
    _name = 'gi.type.price'
    _description = 'Tipo de precio Gamma'

    name = fields.Char(string="Nombre", required=True)
    code = fields.Selection([
        ('U', 'Unidades'),
        ('C', 'Cajas'),
        ('P', 'Palet')
    ], string="Código", required=True)