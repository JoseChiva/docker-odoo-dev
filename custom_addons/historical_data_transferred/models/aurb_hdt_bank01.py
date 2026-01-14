from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtBank01(models.Model):
    _name = "aurb.hdt.bank01"
    _description = "AURB Bank01"
    _rec_name = "name"
    _order = "iban asc"

    name = fields.Char(index=True, required=True)
    empresa = fields.Char()
    subcta = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company",string='Empresa nombre')
    subcta_id = fields.Many2one("aurb.hdt.bank", string= 'Subcuenta nº')
    iban = fields.Char()
    swift = fields.Char()
    sufn19 = fields.Char()
    sufn32 = fields.Char()
    sufn34 = fields.Char()
    sufn43 = fields.Char()
    sufn58 = fields.Char()
    sufn58c = fields.Char()
    inen58 = fields.Char()
    cobcomis = fields.Float()
    cobmincom = fields.Float()
    cobcorreo = fields.Float()
    cobcomiva = fields.Char()
    dtocomis = fields.Float()
    dtointer = fields.Float()
    dtomincom = fields.Float()
    dtocorreo = fields.Float()
    dtocomiva = fields.Char()
    ejeendoc = fields.Char()
    gsconci = fields.Char()
    gsconci_data = fields.Date()
    gscash = fields.Char()
    gscash_data = fields.Date()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.iban != False:
                view_name += ' ' + record.iban
            record.display_name = view_name
