from odoo import models, fields, api, tools, exceptions
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmSaleOrder(models.Model):
    _inherit = "sale.order"

    res_partner_contact = fields.Many2one("res.partner", string="Persona de contacto",
                                          domain="[('is_company','=',False),('type','=','contact'),('parent_id.id','=',partner_id)]")

    num_contract = fields.Char()

    type_transport = fields.Selection(
        [("", ""), ("var1", "+Trailer"), ("var2", "+Camion"), ("var3", "+Reparto")],
        default="",
        String="Tipo transporte")

    @api.onchange('type_transport')
    def _onchange_type_transport(self):
        lines_to_recompute = self._get_update_prices_lines()
        lines_to_recompute.invalidate_recordset(['pricelist_item_id'])
        lines_to_recompute._compute_price_unit()

    @api.onchange('order_line')
    def _onchange_lines(self):
        for head in self:
            for line in head.order_line:
                if line.num_contract:
                    head.num_contract = line.num_contract

    @api.model
    def create(self, vals):
        result = super().create(vals)
        # for head in result:
        #     if (head.pedido_con_error()):
        #         raise exceptions.ValidationError(
        #             "Se han encontrado líneas con contrato y sin contrato o con contrato diferente dentro del mismo documento")
        return result

    def write(self, vals):
        result = super(AurbCmSaleOrder, self).write(vals)
        # for head in self:
        #     if (head.pedido_con_error()):
        #         raise exceptions.ValidationError(
        #             "Se han encontrado líneas con contrato y sin contrato o con contrato diferente dentro del mismo documento")
        return result

    def pedido_con_error(self):
        linea_sin_contrato = False
        linea_con_contrato = ''
        linea_multiple_contrato = False
        for head in self:
            for line in head.order_line:
                if (line.num_contract):
                    if (linea_con_contrato == ''):
                        linea_con_contrato = line.num_contract
                    else:
                        if (linea_con_contrato != line.num_contract):
                            linea_multiple_contrato = True
                else:
                    linea_sin_contrato = True
        if ((linea_sin_contrato and linea_con_contrato != '') or linea_multiple_contrato == True):
            return True
        else:
            return False

    def _get_invoice_grouping_keys(self):
        return ['company_id', 'partner_id', 'currency_id', 'invoice_payment_term_id', 'num_contract']

    def _prepare_invoice(self):
        values = super()._prepare_invoice()
        if (self.num_contract):
            values['num_contract'] = self.num_contract
        else:
            values['num_contract'] = ''
        return values
