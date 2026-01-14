# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Auren_Cm_ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']


# Ampliación de descuentos a nivel de líneas
    group_extended_discount = fields.Boolean(
        default=False, string="Descuento de venta ampliado", config_parameter='multi_discount_sale.group_extended_discount', implied_group='multi_discount_sale.group_extended_discount')

    group_extended_discount_1 = fields.Boolean(
        default=False, string="Activar descuento 1", config_parameter='multi_discount_sale.group_extended_discount_1', implied_group='multi_discount_sale.group_extended_discount_1')
    group_extended_discount_2 = fields.Boolean(
        default=False, string="Activar descuento 2", config_parameter='multi_discount_sale.group_extended_discount_2', implied_group='multi_discount_sale.group_extended_discount_2')
    group_extended_discount_3 = fields.Boolean(
        default=False, string="Activar descuento 3", config_parameter='multi_discount_sale.group_extended_discount_3', implied_group='multi_discount_sale.group_extended_discount_3')
    group_extended_discount_4 = fields.Boolean(
        default=False, string="Activar descuento 4", config_parameter='multi_discount_sale.group_extended_discount_4', implied_group='multi_discount_sale.group_extended_discount_4')
    group_extended_discount_5 = fields.Boolean(
        default=False, string="Activar descuento 5", config_parameter='multi_discount_sale.group_extended_discount_5', implied_group='multi_discount_sale.group_extended_discount_5')
    group_extended_discount_6 = fields.Boolean(
        default=False, string="Activar descuento 6", config_parameter='multi_discount_sale.group_extended_discount_6', implied_group='multi_discount_sale.group_extended_discount_6')

    desc_group_extended_discount_1 = fields.Char(
        default=False, string="Descripción descuento 1", config_parameter='multi_discount_sale.desc_group_extended_discount_1')
    desc_group_extended_discount_2 = fields.Char(
        default=False, string="Descripción descuento 2", config_parameter='multi_discount_sale.desc_group_extended_discount_2')
    desc_group_extended_discount_3 = fields.Char(
        default=False, string="Descripción descuento 3", config_parameter='multi_discount_sale.desc_group_extended_discount_3')
    desc_group_extended_discount_4 = fields.Char(
        default=False, string="Descripción descuento 4", config_parameter='multi_discount_sale.desc_group_extended_discount_4')
    desc_group_extended_discount_5 = fields.Char(
        default=False, string="Descripción descuento 5", config_parameter='multi_discount_sale.desc_group_extended_discount_5')
    desc_group_extended_discount_6 = fields.Char(
        default=False, string="Descripción descuento 6", config_parameter='multi_discount_sale.desc_group_extended_discount_6')

    operation_discount_1 = fields.Selection(required=True, string="Operación descuento 1", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_discount_1')

    operation_discount_2 = fields.Selection(required=True, string="Operación descuento 2", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_discount_2')

    operation_discount_3 = fields.Selection(required=True, string="Operación descuento 3", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_discount_3')

    operation_discount_4 = fields.Selection(required=True, string="Operación descuento 4", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_discount_4')

    operation_discount_5 = fields.Selection(required=True, string="Operación descuento 5", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_discount_5')

    operation_discount_6 = fields.Selection(required=True, string="Operación descuento 6", selection=[
        ('inc', 'Incrementa'),
        ('dec', 'Decrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_discount_6')

    type_discount = fields.Selection(required=True, string="Tipo", selection=[
        ('sum', 'Sumado'),
        ('app', 'Apilado'),
    ], default="app", config_parameter='multi_discount_sale.type_discount')


# Ampliación de descuentos cabecera
    group_head_extended_discount = fields.Boolean(
        default=False, string="Descuento de venta ampliado cabecera", config_parameter='multi_discount_sale.group_head_extended_discount', implied_group='multi_discount_sale.group_head_extended_discount')

    add_vat_line_discount = fields.Boolean(string="Añadir Vat línea de descuento",
                                           config_parameter='multi_discount_sale.add_vat_line_discount')

    group_head_extended_discount_1 = fields.Boolean(
        default=False, string="Activar head descuento 1", config_parameter='multi_discount_sale.group_head_extended_discount_1', implied_group='multi_discount_sale.group_head_extended_discount_1')
    group_head_extended_discount_2 = fields.Boolean(
        default=False, string="Activar head descuento 2", config_parameter='multi_discount_sale.group_head_extended_discount_2', implied_group='multi_discount_sale.group_head_extended_discount_2')
    group_head_extended_discount_3 = fields.Boolean(
        default=False, string="Activar head descuento 3", config_parameter='multi_discount_sale.group_head_extended_discount_3', implied_group='multi_discount_sale.group_head_extended_discount_3')
    group_head_extended_discount_4 = fields.Boolean(
        default=False, string="Activar head descuento 4", config_parameter='multi_discount_sale.group_head_extended_discount_4', implied_group='multi_discount_sale.group_head_extended_discount_4')
    group_head_extended_discount_5 = fields.Boolean(
        default=False, string="Activar head descuento 5", config_parameter='multi_discount_sale.group_head_extended_discount_5', implied_group='multi_discount_sale.group_head_extended_discount_5')
    group_head_extended_discount_6 = fields.Boolean(
        default=False, string="Activar head descuento 6", config_parameter='multi_discount_sale.group_head_extended_discount_6', implied_group='multi_discount_sale.group_head_extended_discount_6')

    product_discount_1_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='multi_discount_sale.product_discount_1_id')
    product_discount_2_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='multi_discount_sale.product_discount_2_id')
    product_discount_3_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='multi_discount_sale.product_discount_3_id')
    product_discount_4_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='multi_discount_sale.product_discount_4_id')
    product_discount_5_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='multi_discount_sale.product_discount_5_id')
    product_discount_6_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='multi_discount_sale.product_discount_6_id')

    desc_group_head_extended_discount_1 = fields.Char(
        default=False, string="Descripción descuento 1", config_parameter='multi_discount_sale.desc_group_head_extended_discount_1')
    desc_group_head_extended_discount_2 = fields.Char(
        default=False, string="Descripción descuento 2", config_parameter='multi_discount_sale.desc_group_head_extended_discount_2')
    desc_group_head_extended_discount_3 = fields.Char(
        default=False, string="Descripción descuento 3", config_parameter='multi_discount_sale.desc_group_head_extended_discount_3')
    desc_group_head_extended_discount_4 = fields.Char(
        default=False, string="Descripción descuento 4", config_parameter='multi_discount_sale.desc_group_head_extended_discount_4')
    desc_group_head_extended_discount_5 = fields.Char(
        default=False, string="Descripción descuento 5", config_parameter='multi_discount_sale.desc_group_head_extended_discount_5')
    desc_group_head_extended_discount_6 = fields.Char(
        default=False, string="Descripción descuento 6", config_parameter='multi_discount_sale.desc_group_head_extended_discount_6')

    operation_head_discount1 = fields.Selection(required=True, string="Operación descuento 1", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_head_discount1')

    operation_head_discount2 = fields.Selection(required=True, string="Operación descuento 2", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_head_discount2')

    operation_head_discount3 = fields.Selection(required=True, string="Operación descuento 3", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_head_discount3')

    operation_head_discount4 = fields.Selection(required=True, string="Operación descuento 4", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_head_discount4')

    operation_head_discount5 = fields.Selection(required=True, string="Operación descuento 5", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_head_discount5')

    operation_head_discount6 = fields.Selection(required=True, string="Operación descuento 6", selection=[
        ('inc', 'Incrementa'),
        ('dec', 'Decrementa'),
    ], default="dec", config_parameter='multi_discount_sale.operation_head_discount6')

    @api.onchange('group_extended_discount')
    def _change_group_extended_discount(self):
        for conf in self:
            if (conf.group_extended_discount == False):
                conf.group_extended_discount_1 = False
                conf.group_extended_discount_2 = False
                conf.group_extended_discount_3 = False
                conf.group_extended_discount_4 = False
                conf.group_extended_discount_5 = False
                conf.group_extended_discount_6 = False

    @api.onchange('group_head_extended_discount')
    def _change_group_extended_discount(self):
        for conf in self:
            if (conf.group_head_extended_discount == False):
                conf.group_head_extended_discount_1 = False
                conf.group_head_extended_discount_2 = False
                conf.group_head_extended_discount_3 = False
                conf.group_head_extended_discount_4 = False
                conf.group_head_extended_discount_5 = False
                conf.group_head_extended_discount_6 = False
