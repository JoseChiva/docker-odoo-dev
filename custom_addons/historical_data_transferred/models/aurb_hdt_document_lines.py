from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtDocumentLines(models.Model):
    _name = "aurb.hdt.document.lines"
    _description = "AURB Document Lines"

    name = fields.Char(index=True, required=True)
    empresa = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company",string = "empresa_id")
    ejercicio = fields.Integer()
    tipo_movimiento = fields.Selection(
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

    linea_pedido = fields.Integer()
    
    articulo = fields.Char()
    articulo_id = fields.Many2one("aurb.hdt.items",string = "articulo_id")
    manual_desc_ids = fields.One2many(
    "aurb.hdt.document.lines.manual.desc", "documento_id", string="manual_desc_ids")

    acumula = fields.Integer()
    cantidad = fields.Float()
    bultos = fields.Float()

    precio = fields.Float()
    precio_iva = fields.Float()
    tipo_precio = fields.Integer()
    descuento_1 = fields.Float()
    descuento_2 = fields.Float()
    descuento_3 = fields.Float()
    comision_1 = fields.Float()
    comision_2 = fields.Float()
    comision_3 = fields.Float()

    tipo_iva = fields.Integer()
    variante = fields.Char()
    iva = fields.Float()
    pedido = fields.Integer()
    presupuesto = fields.Integer()
    recargo_e = fields.Float()
    precio_coste = fields.Float()
    pts_kl = fields.Float()
    aplic_pt_kl = fields.Integer()
    total_linea = fields.Float()
    total_linea_base = fields.Float()
    total_linea_euro = fields.Float()
    moneda_id = fields.Many2one("aurb.hdt.currency",string='moneda_id')

    cambio = fields.Float()
    cambio_euro = fields.Float()

    almacen_id = fields.Many2one("aurb.hdt.warehouse", string="almacen_id")
    #Relación modelos líneas-cabecera.
    documento_id = fields.Many2one("aurb.hdt.document", string="documento_id")

    subcta = fields.Char()
    linea_producto = fields.Integer()
    
    notes_ids = fields.One2many(
        "aurb.hdt.order.notes.lines", "documento_id", string="Observaciones líneas")
    measures_ids = fields.One2many(
        "aurb.hdt.order.manual.measures", "linea_documento_id", string="Medidas manuales")

    articulo_des = fields.Char(compute='_compute_articulo_desc')
 
    @api.depends('articulo_id')
    def _compute_articulo_desc(self):
   
        for record in self:
            record.articulo_des='VACIO'
            for  item0 in record.manual_desc_ids:  
                if item0 != False:
                    for desc0 in item0:
                        record.articulo_des = desc0.descripcion
            for item in record.articulo_id:
                if item != False:
                    for desc in item.items_desc_ids:
                        record.articulo_des = desc.descripcion    
                        
   

 
 
 
 
 
 
 
 
 
 
 

 
 
 
 
 
 
 
 
 