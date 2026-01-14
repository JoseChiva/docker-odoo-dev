from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtDocumentLinesManualDescription(models.Model):
    _name = "aurb.hdt.document.lines.manual.desc"
    _description = "AURB Lines's document Manual Description"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")

    ejercicio = fields.Integer()

    documento_id = fields.Many2one("aurb.hdt.document.lines")

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
   
    
    
    #@api.depends('name')
    #def _compute_display_name(self):
    #    for record in self:
    #        view_name = record.name
    #        if record.tipo_doc != False:
    #            view_name = record.tipo_doc
    #        if record.documento_id != False:
    #            view_name += ' ' + str(record.documento_id)
    #        record.display_name = view_name
        