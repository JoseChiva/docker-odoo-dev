from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtDocument(models.Model):
    _name = "aurb.hdt.document"
    _description = "AURB Document"
    _rec_name = "name"
    _order = "empresa_id,almacen_id,documento desc"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio = fields.Integer()
    subcta = fields.Char()
    ic_id = fields.Many2one("aurb.hdt.partners")
    documento = fields.Integer()
    almacen_id = fields.Many2one("aurb.hdt.warehouse")

    tipo_doc = fields.Selection(
        selection=[
            ('PV', "Pedido venta"),
            ('PP', "Presupuesto"),
            ('PC', "Pedido compra"),
            ('EF', "Entrada fabricación"),
            ('SV', "Albaranes de venta"),
            ('NF', "No facturable venta"),
            ('SF', "Salida fabricación"),
            ('NC', "No facturable compra"),
            ('EC', "Albaranes de Compra"),
            ('FV', "Factura de venta"),
            ('FC', "Factura de compra"),
        ]
    )
    fecha_documento = fields.Date()
    referencia = fields.Char()

    vendedor_1 = fields.Char()
    vendedor_2 = fields.Char()
    vendedor_3 = fields.Char()

    clv_ven_1 = fields.Integer()
    clv_ven_2 = fields.Integer()
    clv_ven_3 = fields.Integer()
    ctd_cuenta = fields.Float()
    ctd_cuenta_base = fields.Float()
    ctd_cuenta_euro = fields.Float()

    moneda_id = fields.Many2one("aurb.hdt.currency")
    cambio = fields.Float()
    cambio_euro = fields.Float()
    situacion = fields.Integer()
    recepcion = fields.Char()
    fecha_valor = fields.Date()
    fecha_entrada = fields.Date()
    usuario_entrada = fields.Char()
    hora_entrada = fields.Char()
    fecha_modifi = fields.Date()
    usuario_modifi = fields.Char()
    hora_modifi = fields.Char()

    campo1 = fields.Char()
    campo2 = fields.Char()
    swift = fields.Char()
    iban = fields.Char()
    adress_id = fields.Many2one('aurb.hdt.partners.address','adress_id')
    notes_ids = fields.One2many(
        "aurb.hdt.document.notes", "documento_id", string="Observaciones")
    # Relacion cabera lineas
    documento_ids = fields.One2many('aurb.hdt.document.lines','documento_id',string ='Líneas documento')
    total_documento_ids = fields.One2many('aurb.hdt.document.total','documento_id',string = 'Total documento')
    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.name != False:
                view_name += ' ' + record.name
            record.display_name = view_name

    #joseplluis 
    nombre_ic = fields.Char(compute='_compute_dispay_nombre_ic')
    
    @api.depends('ic_id')
    def _compute_dispay_nombre_ic(self):
        # Retorna el título de la empresa.
        for record in self:
            record.nombre_ic = 'vacio'
            for ic in record.ic_id:
                record.nombre_ic = ic.name

    # Dirección del documento
    d_orden = fields.Char(string = "Orden", compute = "_compute_display_addres_document")
    d_idioma = fields.Char(string = "Idioma")
    d_tipus = fields.Char(string = "Tipo")
    d_nombre_comercial = fields.Char(string ="Nombre comercial")
    d_nombre_comercial2 = fields.Char(string ="Nombre comercial 2")
    d_direccion = fields.Char(string="Dirección")
    d_direccion2 = fields.Char( string="Dirección 2")
    d_codigo_postal = fields.Char(string="CP")
    d_codigo_postal2 = fields.Char(string="CP2")
    d_poblacion = fields.Char(string="Población")
    d_poblacion2 = fields.Char(string = "Población 2")
    d_provincia = fields.Char(string="Provincia")
    d_dni_nif = fields.Char( string="DNI/NIF")
    d_telefonos = fields.Char(string="Teléfono")
    d_contacte = fields.Char(string="Persona contacto")           

    @api.depends('adress_id')
    def _compute_display_addres_document(self):
        for record in self:
            for dir in record.adress_id:
                record.d_orden = dir.orden
                record.d_idioma = dir.idioma
                record.d_tipus = dir.tipus
                record.d_nombre_comercial = dir.nombre_comercial
                record.d_nombre_comercial2 = dir.nombre_comercial2
                record.d_direccion = dir.direccion
                record.d_codigo_postal = dir.codigo_postal
                record.d_codigo_postal2= dir.codigo_postal2
                record.d_poblacion = dir.poblacion    
                record.d_poblacion2 = dir.poblacion2
                record.d_provincia = dir.provincia
                record.d_dni_nif = dir.dni_nif            
                record.d_telefonos = dir.telefonos
                record.d_contacte = dir.contacte

    #fin joseplluis