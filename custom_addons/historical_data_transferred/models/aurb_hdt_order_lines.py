from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOrderLines(models.Model):
    _name = "aurb.hdt.order.lines"
    _description = "AURB Order Lines"
    _inherits = {
        'aurb.hdt.document.lines': 'document_lines_id'
    }
    
    document_lines_id = fields.Many2one("aurb.hdt.document.lines", required=True, ondelete='cascade', string="documento_lines_id")

    #manual_desc_ids = fields.One2many(
    #"aurb.hdt.document.lines.manual.desc", "documento_id", string="Manual Desc")

    # name = fields.Char(string="doc", index=True, required=True)

    # empresa = fields.Integer(string="empresa")
    # empresa_id = fields.Many2one("aurb.hdt.company", string="emp")
    # ejercicio = fields.Integer()
    # tipo_movimiento = fields.Selection(
    #     selection=[
    #         ('PV', "Pedido venta"),
    #         ('PP ', "Presupuesto"),
    #         ('PC', "Pedido compra")
    #     ]
    # )

    # pedido = fields.Integer()
    
    pedido_id = fields.Many2one('aurb.hdt.order',string = "pedido_id")
     
    # linea_pedido = fields.Integer()

    clv_ped = fields.Integer()
    fecha_servicio = fields.Date()
    # articulo = fields.Char()
    # acumula = fields.Integer()
    # cantidad = fields.Float()
    # bultos = fields.Float()
    cantidad_s = fields.Float()
    bultos_s = fields.Float()

    # precio = fields.Float()
    # precio_iva = fields.Float()
    # tipo_precio = fields.Integer()
    # descuento_1 = fields.Float()
    # descuento_2 = fields.Float()
    # descuento_3 = fields.Float()
    # comision_1 = fields.Float()
    # comision_2 = fields.Float()
    # comision_3 = fields.Float()

    # tipo_iva = fields.Integer()
    # variante = fields.Char()
    # iva = fields.Float()
    recargo_e = fields.Float()
    precio_coste = fields.Float()
    pts_kl = fields.Float()
    aplic_pt_kl = fields.Integer()
    total_linea = fields.Float()
    total_linea_base = fields.Float()
    total_linea_euro = fields.Float()
    # moneda_id = fields.Many2one("aurb.hdt.currency")

    # cambio = fields.Float()
    # cambio_euro = fields.Float()
    # almacen = fields.Char()
    # subcta = fields.Char()
    # linea_producto = fields.Integer()

    clv_sub = fields.Integer()
    fecha_documento = fields.Date()
    presupuesto = fields.Integer()
    linea_presupuesto = fields.Integer()

    triangulado = fields.Char()
    lote_interno = fields.Char()
    od_linea = fields.Integer()
    codexpe = fields.Char()
    campo1 = fields.Char()
    campo2 = fields.Char()
    porcentaje = fields.Float()
    eur_kg = fields.Float()

    notes_ids = fields.One2many(
        "aurb.hdt.order.notes.lines", "documento_id", string="Observaciones líneas")
    measures_ids = fields.One2many(
        "aurb.hdt.order.manual.measures", "linea_documento_id", string="Medidas manuales")



    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.pedido_id.tipo_doc != False:
                view_name = record.pedido_id.tipo_doc
            if record.pedido_id.documento != False:
                view_name += ' ' + str(record.pedido_id.documento)
            if record.linea_pedido != False:
                view_name += ' ' + str(record.linea_pedido)
            record.display_name = view_name
    #joseplluis 
    #articuloor_des = fields.Char(compute='_compute_articulo_des')
 #
    #@api.depends('articulo_id')
    #def _compute_articulo_des(self):
    ## Retorna el título de la empresa.
    #    for record in self:
    #        record.articuloor_des='VACIO'
    #        for  item0 in record.manual_desc_ids:  
    #            if item0 != False:
    #                for desc0 in item0:
    #                    record.articuloor_des = desc0.descripcion
    #        for item in record.articulo_id:
    #            if item != False:
    #                for desc in item.items_desc_ids:
    #                    record.articuloor_des = desc.descripcion    
    #                    loop_executed = True
            
                
                
                        
             
    
    
    
    
    
    
    