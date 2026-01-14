from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOrder(models.Model):
    _name = "aurb.hdt.order"
    _description = "AURB Order"
    _inherits = {
        'aurb.hdt.document': 'documento_id'
    }
    
    documento_id = fields.Many2one("aurb.hdt.document", required=True, ondelete='cascade', string='documento_id')
    lines_ids =fields.One2many('aurb.hdt.order.lines','pedido_id',string='Lines')
    clv_sub = fields.Integer()
    orden = fields.Integer()
    clv_ped = fields.Integer()

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
    agencia_transporte = fields.Integer()
    pedido_definitivo = fields.Integer()
    albaran_factura = fields.Integer()
    alternativo = fields.Integer()
    subcta_facturacion = fields.Char()
    subcta_contable = fields.Char()
    linea_producto = fields.Integer()
    intervalo_factura = fields.Integer()

    origen_oferta = fields.Char()
    triangulado = fields.Char()
    ccc1 = fields.Char()
    ccc2 = fields.Char()
    dc = fields.Char()
    numero_cuenta = fields.Char()

    codexpe = fields.Char()

    status_doc = fields.Selection(
        selection=[
            ('borrador', "Borrador"),
            ('enviado', "Enviado"),
            ('entregado', "Entregado"),
        ]
    )
    total_bruto = fields.Float()
    total_descuentos = fields.Float()
    total_impuestos = fields.Float()
    total_neto_euros = fields.Float()

    #lines_ids = fields.One2many(
    #    "aurb.hdt.order.lines", "documento_id", string="Lines")
    
    

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.tipo_doc != False:
                view_name = record.tipo_doc
            if record.documento != False:
                view_name += ' ' + str(record.documento)
            record.display_name = view_name
