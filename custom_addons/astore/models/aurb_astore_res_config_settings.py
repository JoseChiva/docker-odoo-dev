# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Auren_aStore_ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    max_amount_simplified_invoice = fields.Float(
        default=False,  config_parameter='astore.max_amount_simplified_invoice')

    simplified_invoice_partner_id = fields.Many2one(
        "res.partner",  config_parameter='astore.simplified_invoice_partner_id')

    max_amount_cash = fields.Float(
        default=400, config_parameter='astore.max_amount_cash')

    auto_posted_account_move = fields.Boolean(
        default=False, config_parameter='astore.auto_posted_account_move')

    group_direct_invoice = fields.Boolean(
        default=False, string="Activar botón  de factura directa", config_parameter='astore.group_direct_invoice', implied_group='astore.group_direct_invoice')
