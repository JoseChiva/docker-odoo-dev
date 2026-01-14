from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtAccountingEntries(models.Model):
    _name = "aurb.hdt.accounting.entries"
    _description = "AURB Accounting Entries"
    _rec_name = "name"
    _order = "asiento asc"

    partner_manual_ids = fields.One2many('aurb.hdt.partners.manual','asiento_id')
    cartera_fra_ids = fields.One2many('aurb.hdt.incoming.payments.original','asiento_id')
    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company", string = 'empresa_id')
    ejercicio_id = fields.Many2one("aurb.hdt.exercices", string = 'ejercicio_id')
    asiento = fields.Integer()
    orden = fields.Integer()
    fecha_entrada = fields.Date()
    fecha_contable = fields.Date()
    usuario = fields.Char()
    subcta_id = fields.Many2one("aurb.hdt.subaccounts", string = 'subcta_id')
    importe_debe = fields.Float()
    debe_base = fields.Float()
    debe_euro = fields.Float()
    importe_haber = fields.Float()
    haber_base = fields.Float()
    haber_euro = fields.Float()
    tipo = fields.Char()
    moneda_id = fields.Many2one("aurb.hdt.currency", string ='moneda_id')
    cambio = fields.Float()
    cambio_euro = fields.Float()
    fecha_valor = fields.Date()
    concepto = fields.Char()
    descripcion_1 = fields.Char()
    descripcion_2 = fields.Char()
    documento = fields.Char()
    subcta_contrap_id = fields.Many2one("aurb.hdt.subaccounts", string = 'subcta_contrap_id')
    impreso = fields.Char()
    fecha_impreso = fields.Date()
    asiento_definitivo = fields.Integer()
    orden_definitivo = fields.Integer()
    diario = fields.Integer()
    procedencia = fields.Integer()
    estado = fields.Char()
    centro = fields.Char()
    p_s = fields.Char()
    p_sd = fields.Char()
    triangulado = fields.Char()
    iden = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.asiento != False:
                view_name += ' ' + str(record.asiento)
            record.display_name = view_name
