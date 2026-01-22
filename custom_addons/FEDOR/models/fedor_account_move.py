# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models, api
from odoo.tools import formatLang, format_date

from markupsafe import Markup, escape


class FedorAccountMove(models.Model):
    _inherit = 'account.move'

    currency_rate = fields.Float(
        inverse='_inverse_currency_rate',
        help="Currency rate from company currency to document currency.", digits=(16, 6),
    )

    @api.depends('currency_rate')
    def _inverse_currency_rate(self):
        for invoice in self:
            if (invoice.move_type in ('in_invoice', 'in_refund')):
                if (invoice.currency_rate):
                    for line in invoice.invoice_line_ids:
                        line.currency_rate = 1/invoice.currency_rate

    @api.model
    def create(self, vals):
        records = super().create(vals)
        for invoice in records:
            if (invoice.move_type in ('in_invoice', 'in_refund')):
                multi_change_div = False
                message_change_div = ""
                if (invoice.invoice_line_ids):
                    for invoice_line in invoice.invoice_line_ids:
                        if (invoice_line.product_id):
                            product = invoice_line.product_id
                            if (product.seller_ids):
                                for product_supplierinfo in product.seller_ids:
                                    if (
                                        product_supplierinfo.partner_id == invoice.partner_id and
                                        product_supplierinfo.currency_id == invoice.currency_id and
                                        invoice.currency_id != self.env.company.currency_id
                                    ):
                                        if (product_supplierinfo.type_change):
                                            message_change_div += _("<li style='background-color: red;color:white'> Producto : [%(product_ref)s] %(product_name)s tipo de cambio %(type_change)s </li>",
                                                                    product_ref=invoice_line.product_id.default_code,
                                                                    product_name=invoice_line.product_id.name,
                                                                    type_change=str(
                                                                        product_supplierinfo.type_change))

                                            if (invoice.currency_rate != False):
                                                if (product_supplierinfo.type_change != invoice.currency_rate):
                                                    multi_change_div = True
                                            if (product_supplierinfo.type_change > invoice.currency_rate):
                                                invoice.currency_rate = product_supplierinfo.type_change
                    if (multi_change_div):
                        odoobot = self.env.ref(
                            'base.partner_root')

                        message_change_div = Markup(
                            "<ul>"+message_change_div+"</ul>")
                        invoice.message_post(
                            body=message_change_div, subject="Se han encontrado tipos de cambio diferentes", message_type='comment',
                            author_id=odoobot.id)

        return records
