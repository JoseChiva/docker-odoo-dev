from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtDocumentNotes(models.Model):
    _name = "aurb.hdt.document.notes"
    _description = "AURB Document Observaciones"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")

    ejercicio = fields.Integer()

    documento = fields.Integer()
    documento_id = fields.Many2one(
        "aurb.hdt.document", required=True)

    tipo_doc = fields.Selection(
        selection=[
            ('PV', "Pedido venta"),
            ('PP ', "Presupuesto"),
            ('PC', "Pedido compra"),
            ('EF', "Entrada fabricación"),
            ('SV', "Albaranes de venta"),
            ('NF', "No facturable venta"),
            ('SF', "Salida fabricación"),
            ('NC', "No facturable compra"),
            ('EC', "Albaranes de Compra"),
        ]
    )
    almacen_id = fields.Many2one("aurb.hdt.warehouse")
    orden = fields.Integer()
    descripcion = fields.Char()
    clv_man = fields.Integer()
    facturado = fields.Integer()
