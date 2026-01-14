from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtSeller(models.Model):
    _name = "aurb.hdt.seller"
    _description = "AURB Seller"
    _rec_name = "name"
    _order = "empresa_id asc,subcta desc"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta = fields.Char()
    linea_producto = fields.Integer()
    clv_ven = fields.Integer()
    iva = fields.Float()
    irpf = fields.Float()

    comisiones = fields.One2many(
        "aurb.hdt.seller.commission", "subcta_id", string="Comisiones")

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.subcta != False:
                view_name = record.subcta
            record.display_name = view_name