from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtPartnersAccount(models.Model):
    _name = "aurb.hdt.partners.account"
    _description = "AURB Partners Account"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company")
    subcta_id = fields.Many2one("aurb.hdt.partners")
    linea_producto = fields.Integer()
    clv_sub = fields.Integer()
    tarifa = fields.Char()
    portes = fields.Integer()
    agencia_transporte = fields.Integer()
    tipo_iva = fields.Integer()
    tipo_iva_alt = fields.Integer()
    albaran_valorado = fields.Integer()
    albaran_factura = fields.Integer()
    pedido_albaran = fields.Integer()
    intervalo_factura = fields.Integer()
    copias_albaran = fields.Integer()
    copias_factura = fields.Integer()
    descuento_p_pago = fields.Float()
    descripcion_dto_2 = fields.Char()
    descuento_2 = fields.Float()
    descripcion_dto_3 = fields.Char()
    descuento_3 = fields.Float()
    cl_circ_oferta = fields.Char()
    cargo_financiero = fields.Float()
    cargo_fin_dias = fields.Integer()
    descripcion_car_2 = fields.Char()
    cargo_2 = fields.Float()
    irpf = fields.Float()
    aplic_irpf = fields.Integer()
    vendedor_1 = fields.Char()
    vendedor_2 = fields.Char()
    vendedor_3 = fields.Char()
    facturar_envase = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.subcta_id.subcta != False:
                view_name += ' ' + record.subcta_id.subcta
            record.display_name = view_name