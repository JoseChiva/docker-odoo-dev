from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtInvoice(models.Model):
    _name = "aurb.hdt.invoice"
    _description = "AURB Invoice"
    _inherits = {
        'aurb.hdt.document': 'document_id'
    }

    document_id = fields.Many2one(
        "aurb.hdt.document", required=True, ondelete='cascade')

    clv_sub = fields.Integer()
    orden = fields.Integer()
    paquetes = fields.Integer()
    tipo_forma_pago = fields.Char()

    status_doc = fields.Selection(
        selection=[
            ('borrador', "Borrador"),
            ('facturado', "Facturado"),
            ('contabilizado', "Contabilizado"),
        ]
    )
    total_bruto = fields.Float(string='Total Bruto')
    total_descuentos = fields.Float(string='Total Descuentos')
    total_impuestos = fields.Float(string='Total Impuestos')
    total_neto_euros = fields.Float(string='Total Neto Euros')        
    numero_recibos = fields.Integer()
    primer_intervalo = fields.Integer()
    otros_intervalos = fields.Integer()
    dia_fijo_pago_1 = fields.Integer()
    dia_fijo_pago_2 = fields.Integer()
    descuento_p_pago = fields.Float()
    descuento_2 = fields.Float()
    descuento_3 = fields.Float()
    tarifa = fields.Char()
    categoria = fields.Char()
    tipo_iva = fields.Integer()
    cargo_financiero = fields.Float()
    cargo_fin_dias = fields.Integer()
    cargo_2 = fields.Float()
    irpf = fields.Float()
    aplic_irpf = fields.Integer()
    portes = fields.Integer()
    transporte = fields.Integer()
    agencia_transporte = fields.Integer()
    asiento = fields.Integer()
    asiento_id = fields.Many2one('aurb.hdt.accounting.entries', string='asiento_id')
    alternativo = fields.Integer()
    impresa = fields.Integer()
    subcta_facturacion = fields.Char()
    subcta_contable = fields.Char()
    linea_producto = fields.Integer()
    triangulado = fields.Char()
    ccc1 = fields.Char()
    ccc2 = fields.Char()
    dc = fields.Char()
    numero_cuenta = fields.Char()
    lines_ids = fields.One2many(
        "aurb.hdt.delivery.lines", "factura_id", string="Lines")
    
    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.tipo_doc != False:
                view_name = record.tipo_doc
            if record.documento != False:
                view_name += ' ' + str(record.documento)
            record.display_name = view_name

    #josep lluis
    
    @property 
    def address_id(self):
        for record in self:
            ids =[("name", "=", f"{self.empresa_id.empresa}_{self.subcta}_{self.orden}")]
            return self.env["aurb.hdt.partners.address"].search(ids)
    
    cobrospdf_ids = fields.One2many('aurb.hdt.incoming.payments.original', compute= '_compute_cobrospdf_id')
    @api.depends('asiento_id')
    def _compute_cobrospdf_id(self):
        for record in self:
            record.cobrospdf_ids = False
            for asiento in record.asiento_id:
                record.cobrospdf_ids = asiento.cartera_fra_ids

   
