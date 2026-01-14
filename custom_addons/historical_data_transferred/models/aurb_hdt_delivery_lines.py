from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtOrderLines(models.Model):
    _name = "aurb.hdt.delivery.lines"
    _description = "AURB Delivery Lines"
    _inherits = {
        'aurb.hdt.document.lines': 'document_lines_id'
    }

    document_lines_id = fields.Many2one("aurb.hdt.document.lines", required=True, ondelete='cascade', string="document_lines_id")

    albaran_id = fields.Many2one("aurb.hdt.delivery", required=True, string = 'albaran_id' )

    linea_albaran = fields.Integer()

    clv_ped = fields.Integer()
    fecha_servicio = fields.Date()
    cantidad_s = fields.Float()
    bultos_s = fields.Float()
    recargo_e = fields.Float()
    precio_coste = fields.Float()
    pts_kl = fields.Float()
    aplic_pt_kl = fields.Integer()
    total_linea = fields.Float()
    total_linea_base = fields.Float()
    total_linea_euro = fields.Float()
    # moneda_id = fields.Many2one("aurb.hdt.currency")
    clv_sub = fields.Integer()
    fecha_documento = fields.Date()
    factura = fields.Integer()
    factura_id = fields.Many2one("aurb.hdt.invoice")
    linea_factura = fields.Integer()
    fecha_factura = fields.Date()
    centro_coste = fields.Char()

    gastos_exped = fields.Float()
    facturado = fields.Integer()
    
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
            view_name = record.albaran_id.document_id.name
            if record.albaran_id.tipo_doc != False:
                view_name = record.albaran_id.tipo_doc
            if record.albaran_id.documento != False:
                view_name += ' ' + str(record.albaran_id.documento)
            if record.linea_albaran != False:
                view_name += ' ' + str(record.linea_albaran)
            record.display_name = view_name

    @api.depends('cantidad_s', 'precio', 'descuento_1', 'descuento_2', 'descuento_3')
    def _precio(self):
        for linea in self:
            linea.total_linea = linea.cantidad_s * linea.precio
            if linea.descuento_1 != False:
                linea.total_linea -= ((linea.cantidad_s * linea.precio * linea.descuento_1) / 100)
            if linea.descuento_2 != False:
                linea.total_linea -= ((linea.cantidad_s * linea.precio * linea.descuento_2) / 100)
            if linea.descuento_3 != False:
                linea.total_linea -= ((linea.cantidad_s * linea.precio * linea.descuento_3) / 100)
