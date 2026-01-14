from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtDelivery(models.Model):
    _name = "aurb.hdt.delivery"
    _description = "AURB Delivery"
    _inherits = {
        'aurb.hdt.document': 'documento_id'
    }

    documento_id = fields.Many2one(
        "aurb.hdt.document", required=True, ondelete='cascade')

    clv_sub = fields.Integer()
    orden = fields.Integer()

    paquetes = fields.Integer()

    facturable = fields.Integer()

    tipo_forma_pago = fields.Char()
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

    albaran_factura = fields.Integer()
    alternativo = fields.Integer()
    subcta_facturacion = fields.Char()
    subcta_contable = fields.Char()
    linea_producto = fields.Integer()
    intervalo_factura = fields.Integer()

    factura = fields.Integer()
    fecha_factura = fields.Date()
    facturado = fields.Integer()

    triangulado = fields.Char()
    ccc1 = fields.Char()
    ccc2 = fields.Char()
    dc = fields.Char()
    numero_cuenta = fields.Char()

    codexpe = fields.Char()

    lines_ids = fields.One2many(
        "aurb.hdt.delivery.lines", "albaran_id", string="Lines")
    #manual_desc_ids = fields.One2many(
    #    "aurb.hdt.order.manual.desc", "documento_id", string="Manual Desc")
    notes_ids = fields.One2many(
        "aurb.hdt.document.notes", "documento_id", string="Observaciones")
    
    status_doc = fields.Selection(
        selection=[
            ('borrador', "Borrador"),
            ('enviado', "Enviado"),
            ('facturado', "Facturado"),
        ]
    )
    total_bruto = fields.Float(string='Total Bruto', compute='_compute_amounts',store=True)
    total_descuentos = fields.Float(string='Total Descuentos', compute='_compute_amounts',store=True)
    total_impuestos = fields.Float(string='Total Impuestos', compute='_compute_amounts',store=True)
    total_neto_euros = fields.Float(string='Total Neto Euros', compute='_compute_amounts',store=True)
    
    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.documento_id.name
            if record.tipo_doc != False:
                view_name = record.tipo_doc
            if record.documento != False:
                view_name += ' ' + str(record.documento)
            record.display_name = view_name

    @api.depends('lines_ids.precio', 'lines_ids.cantidad', 'lines_ids.descuento_1', 'lines_ids.descuento_2', 'lines_ids.descuento_3', 'lines_ids.total_linea', 'agencia_transporte')
    def _compute_amounts(self):
        for cabecera in self:
            total_bruto = sum(line.precio*line.cantidad for line in cabecera.lines_ids)
            total_descuentos = sum((line.precio*line.descuento_1/100)+(line.precio*line.descuento_2/100)+(line.precio*line.descuento_3/100) for line in cabecera.lines_ids)
            total_impuestos = sum(line.precio*line.cantidad*21/100 for line in cabecera.lines_ids)
            total_neto_euros = total_bruto - total_descuentos + total_impuestos
            cabecera.total_bruto = total_bruto
            cabecera.total_descuentos = total_descuentos
            cabecera.total_impuestos = total_impuestos
            cabecera.total_neto_euros = total_neto_euros
