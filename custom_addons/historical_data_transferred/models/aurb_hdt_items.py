from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtItems(models.Model):
    _name = "aurb.hdt.items"
    _description = "AURB Items"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    codigo = fields.Char()
    clv_art = fields.Integer()
    codigo_a = fields.Char()

    tipo = fields.Integer()
    tipo_art = fields.Char()
    ficha_cerrada = fields.Selection(
        selection=[
            ('0', "Abierto"),
            ('1', "Cerrado"),
        ]
    )
    fecha_baja = fields.Date()

    items_desc_ids = fields.One2many(
     "aurb.hdt.items.desc", "codigo_id", string="Descripciones")
   
   
    items_price_ids = fields.One2many(
        "aurb.hdt.items.price", "codigo_id", string="Precios")

   
   

    items_batch_ids = fields.One2many(
        "aurb.hdt.items.batch", "codigo_id", string="Lotes")

    items_keys_ids = fields.One2many(
        "aurb.hdt.keys", "codigo_id", string="Claves")

    items_batch_piece_ids = fields.One2many(
        "aurb.hdt.items.batch.piece", "codigo_id", string="Lotes")

    items_batch_incident_ids = fields.One2many(
        "aurb.hdt.items.batch.incident", "codigo_id", string="Lotes")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.codigo != False:
                view_name += ' ' + record.codigo
            record.display_name = view_name
