from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtIncomingPaymentsOriginal(models.Model):
    _name = "aurb.hdt.incoming.payments.original"
    _description = "AURB Incoming Payments original"
    _rec_name = "name"
    _order = "empresa_id,documento desc"

    name = fields.Char(index=True, required=True)
    empresa_id = fields.Many2one("aurb.hdt.company")
    ejercicio_id = fields.Many2one("aurb.hdt.exercices")
    subcta = fields.Char()
    asientoc = fields.Integer()
    asiento_id = fields.Many2one('aurb.hdt.accounting.entries', string = 'asiento_id')
    ordenc = fields.Integer()
    asientoliq = fields.Integer()
    ordenliq = fields.Integer()
    fechaliq = fields.Date()
    documento = fields.Integer()
    ordenvto = fields.Integer()
    fechavto = fields.Date()
    importe = fields.Float()
    importeb = fields.Float()
    moneda_id = fields.Many2one("aurb.hdt.currency")

    cambio = fields.Float()
    fechae = fields.Date()
    remesa = fields.Integer()
    fecharem = fields.Date()
    ntalon = fields.Char()
    tipoe = fields.Char()
    banco = fields.Char()

    ordend = fields.Integer()
    comentario = fields.Char()
    serie = fields.Char()
    gastosdev = fields.Float()
    gastosinc = fields.Char()
    vendedor1 = fields.Char()
    vendedor2 = fields.Char()
    vendedor3 = fields.Char()
    impreso = fields.Char()
    ccc1 = fields.Char()
    ccc2 = fields.Char()
    dc = fields.Char()
    numcta = fields.Char()

    iban = fields.Char()
    swift = fields.Char()
    procede = fields.Char()
    destino = fields.Char()
    valorc1 = fields.Char()
    valorc2 = fields.Char()
    valord1 = fields.Float()
    valord2 = fields.Float()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.documento != False:
                view_name += ' ' + str(record.documento)
            record.display_name = view_name