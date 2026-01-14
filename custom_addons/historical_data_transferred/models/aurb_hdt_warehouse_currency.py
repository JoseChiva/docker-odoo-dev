from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbHdtWarehouseCurrency(models.Model):
    _name = "aurb.hdt.warehouse.currency"
    _description = "AURB Warehouse Currency"
    _rec_name = "name"

    name = fields.Char()
    empresa_id = fields.Many2one("aurb.hdt.company",string="empresa")
    almacen_id = fields.Many2one("aurb.hdt.warehouse", string = "almacen")

    moneda_ref_id = fields.Many2one("aurb.hdt.currency",string = "moneda_ref")
    moneda_cons_id = fields.Many2one("aurb.hdt.currency",string = "moneda_cons" )
    subcta_compen = fields.Char()
    subcta_tr = fields.Char()

    diario_tr = fields.Integer()
    concepto_tr = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.name
            if record.empresa_id.titulo != False:
                view_name = record.empresa_id.titulo
            if record.almacen_id.nombre != False:
                view_name += ' ' + record.almacen_id.nombre
            if record.moneda_ref_id.moneda != False:
                view_name += ' ' + str(record.moneda_ref_id.moneda)
            record.display_name = view_name