from odoo import models, fields

class ModelPrueba(models.Model):
    _name = "modelo.prueba"
    _description = "Model prueba"
    namefield = fields.Char(string="Name", required=True)
    descriptionfield = fields.Char()