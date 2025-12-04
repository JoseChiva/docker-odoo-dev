from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbaStoreSaleOrder(models.Model):
    _inherit = "sale.order"

    pos_id = fields.Many2one("aurb.astore.pos")
    partner_unidentified = fields.Boolean()
    user_pos = fields.Boolean()

    @api.model
    def create(self, vals):

        records = super().create(vals)

        for sale_order in records:
            current_uid = self._uid
            user = self.sudo().env['res.users'].browse(current_uid)

            if user.pos_id.id != False:
                code = user.pos_id.code
                separator = user.pos_id.separator
                sale_order.name = code+separator+sale_order.name

                amount_total = sale_order.amount_total
                max_amount = 0
                if (sale_order.partner_unidentified == True):
                    val = validate_amount(self, amount_total, max_amount)
                    if (val[0]):
                        raise ValidationError(
                            "El importe de cliente sin indentificar no puede ser superior a :"+str(val[1]))
        return records

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        # defaults.setdefault('user_pos', False)

        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        if user.pos_id.id != False:
            defaults.setdefault('user_pos', True)

            defaults.setdefault('pos_id', user.pos_id.id)
            defaults.setdefault(
                'journal_id', user.pos_id.stock_location_id.journal_id.id)

            simplified_invoice_partner_id = get_user_unidentified(self)
            if (simplified_invoice_partner_id != 0):
                defaults.setdefault(
                    'partner_id', simplified_invoice_partner_id)
                defaults.setdefault('partner_unidentified', True)

        return defaults

    @api.onchange("partner_unidentified")
    def _change_partner_unidentified(self):

        for sale_order in self:
            if (sale_order.partner_unidentified == True):
                sale_order.partner_id = get_user_unidentified(self)

    def create_invoice_auren(self):
        for sale_order in self:
            sale_order.action_confirm()

            for pick in sale_order.picking_ids:
                pick.action_assign()
                pick.button_validate()

            move = sale_order.sudo().env["sale.advance.payment.inv"].create({
                "advance_payment_method": "delivered",
            })
            move.write(
                {'sale_order_ids': [(4, sale_order.id, 0)]})
            move.create_invoices()

            for invoice in sale_order.invoice_ids:
                invoice.action_post()
                return invoice.sudo().action_register_payment()

        return True


def get_user_unidentified(self):
    parameters = self.env['ir.config_parameter'].sudo()
    simplified_invoice_partner_id = int(parameters.get_param(
        'astore.simplified_invoice_partner_id'))
    return simplified_invoice_partner_id


def validate_amount(self, amount, max_amount_simplified_invoice):
    parameters = self.env['ir.config_parameter'].sudo()
    max_amount_simplified_invoice = float(parameters.get_param(
        'astore.max_amount_simplified_invoice'))
    return [max_amount_simplified_invoice < amount, max_amount_simplified_invoice]
