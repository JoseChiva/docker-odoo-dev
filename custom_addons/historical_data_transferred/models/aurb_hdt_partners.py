from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartners(models.Model):
    _name = "aurb.hdt.partners"
    _description = "AURB Partners"
    _rec_name = "name"

    name = fields.Char()
    empresa = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company", string='empresa_id')
    subcta = fields.Char()
    subcta_id = fields.Many2one("aurb.hdt.subaccounts", string ='subcta_id')
    linea_producto = fields.Integer()
    clv_sub = fields.Integer()
    subcta_contable = fields.Char()
    subcta_facturacion = fields.Char()
    
    #subcta_contable_id = fields.Many2one("aurb.hdt.subaccounts", string ='subcta_contable_id')
    #subcta_facturacion_id = fields.Many2one("aurb.hdt.subaccounts", string = 'subcta_facturacion_id')
    zona_comercial = fields.Integer()
    categoria = fields.Char()
    categoria_rappel = fields.Char()
    categoria_oferta = fields.Char()
    ficha_cerrada = fields.Integer()
    fecha_alta = fields.Date()
    fecha_baja = fields.Date()
    subcta_contra = fields.Char()

    num_tarjeta_ids = fields.One2many(
        "aurb.hdt.partners.cards", "subcta_id", string="Tarjetas")

    riesgo_ids = fields.One2many(
        "aurb.hdt.partners.risk", "subcta_id", string="Riesgo")

    contactos_ids = fields.One2many(
        "aurb.hdt.partners.contact", "subcta_id", string="Contactos")
    
    direcciones_ids = fields.One2many(
        "aurb.hdt.partners.address", "subcta_id", string="Direcciones")
    
    contabilidad_ids = fields.One2many(
        "aurb.hdt.partners.account", "subcta_id", string="Contabilidad")
    
    formas_pago_ids = fields.One2many(
        "aurb.hdt.partners.payment.terms", "subcta_id", string="Formas pago")
    
    observaciones_ids = fields.One2many(
        "aurb.hdt.partners.comments", "subcta_id", string="Manual")
    
    manual_ids = fields.One2many(
        "aurb.hdt.partners.manual", "subcta_id", string="Manual")
    
    
    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta != False:
                view_name += ' ' + record.subcta
            record.display_name = view_name