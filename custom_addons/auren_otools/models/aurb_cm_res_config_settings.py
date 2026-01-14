# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Auren_Cm_ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    journal_for_location = fields.Boolean(
        default=False, string="Diario contable por almacén", config_parameter='auren_otools.journal_for_location')

    sale_autorization_management = fields.Boolean(
        default=False, string="Gestión de registro de compradores", config_parameter='auren_otools.sale_autorization_management')

    # Artículos
    group_dim_inv = fields.Boolean(
        default=False, string="Artículos con dimensiones", config_parameter='auren_otools.group_dim_inv', implied_group='auren_otools.group_dim_inv')

    group_dim_var1 = fields.Boolean(
        default=False, string="Gestión con dimensiones var1", config_parameter='auren_otools.group_dim_var1', implied_group='auren_otools.group_dim_var1')
    group_dim_var2 = fields.Boolean(
        default=False, string="Gestión con dimensiones var2", config_parameter='auren_otools.group_dim_var2', implied_group='auren_otools.group_dim_var2')
    group_dim_var3 = fields.Boolean(
        default=False, string="Gestión con dimensiones var3", config_parameter='auren_otools.group_dim_var3', implied_group='auren_otools.group_dim_var3')

    var1_s = fields.Char(string="Nombre dimensión 1",
                         config_parameter='auren_otools.var1_s')
    var2_s = fields.Char(string="Nombre dimensión 2",
                         config_parameter='auren_otools.var2_s')
    var3_s = fields.Char(string="Nombre dimensión 3",
                         config_parameter='auren_otools.var3_s')

    uom_sale = fields.Many2one("uom.uom",
                               help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='auren_otools.uom_sale'
                               )
    uom_sale_2 = fields.Many2one("uom.uom",
                                 help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='auren_otools.uom_sale_2'
                                 )

    uom_sale_3 = fields.Many2one("uom.uom",
                                 help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='auren_otools.uom_sale_3'
                                 )
    uom_sale_4 = fields.Many2one("uom.uom",
                                 help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='auren_otools.uom_sale_4'
                                 )

    formula_s = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='auren_otools.formula_s'
    )
    formula_s_2 = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='auren_otools.formula_s_2'
    )

    formula_s_3 = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='auren_otools.formula_s_3'
    )
    formula_s_4 = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='auren_otools.formula_s_4'
    )

    # Ventas

    group_dim_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones", config_parameter='auren_otools.group_dim_sales', implied_group='auren_otools.group_dim_sales')

    group_dim_var1_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones sales var1", config_parameter='auren_otools.group_dim_var1_sales', implied_group='auren_otools.group_dim_var1_sales')
    group_dim_var2_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones sales var2", config_parameter='auren_otools.group_dim_var2_sales', implied_group='auren_otools.group_dim_var2_sales')
    group_dim_var3_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones sales var3", config_parameter='auren_otools.group_dim_var3_sales', implied_group='auren_otools.group_dim_var3_sales')

    var_readonly_s = fields.Boolean(
        default=False, string="Dimensiones sólo lectura", config_parameter='auren_otools.var_readonly_s')

    group_extended_uom_sale = fields.Boolean(
        default=False, string="Inventario Uom Ampliada", config_parameter='auren_otools.group_extended_uom_sale', implied_group='auren_otools.group_extended_uom_sale')

    group_extended_uom_sale_con = fields.Boolean(
        default=False, string="Visualzar Factor de Conversión en Documentos", config_parameter='auren_otools.group_extended_uom_sale_con', implied_group='auren_otools.group_extended_uom_sale_con')
    group_extended_uom_sale_qty = fields.Boolean(
        default=False, string="Visualizar Cantidad UoM en Documentos", config_parameter='auren_otools.group_extended_uom_sale_qty', implied_group='auren_otools.group_extended_uom_sale_qty')

    # Compras

    group_dim_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones", config_parameter='auren_otools.group_dim_purchase', implied_group='auren_otools.group_dim_purchase')

    group_dim_var1_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones purchase var1", config_parameter='auren_otools.group_dim_var1_purchase', implied_group='auren_otools.group_dim_var1_purchase')
    group_dim_var2_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones purchase var2", config_parameter='auren_otools.group_dim_var2_purchase', implied_group='auren_otools.group_dim_var2_purchase')
    group_dim_var3_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones purchase var3", config_parameter='auren_otools.group_dim_var3_purchase', implied_group='auren_otools.group_dim_var3_purchase')

    var_readonly_p = fields.Boolean(
        default=False, string="Dimensiones sólo lectura", config_parameter='auren_otools.var_readonly_p')

    group_extended_uom_purchase = fields.Boolean(
        default=False, string="Inventario Uom Ampliada", config_parameter='auren_otools.group_extended_uom_purchase', implied_group='auren_otools.group_extended_uom_purchase')

    group_extended_uom_purchase_con = fields.Boolean(
        default=False, string="Visualzar Factor de Conversión en Documentos", config_parameter='auren_otools.group_extended_uom_purchase_con', implied_group='auren_otools.group_extended_uom_purchase_con')
    group_extended_uom_purchase_qty = fields.Boolean(
        default=False, string="Visualizar Cantidad UoM en Documentos", config_parameter='auren_otools.group_extended_uom_purchase_qty', implied_group='auren_otools.group_extended_uom_purchase_qty')

# Ampliación de descuentos a nivel de líneas
    group_extended_discount = fields.Boolean(
        default=False, string="Descuento de venta ampliado", config_parameter='auren_otools.group_extended_discount', implied_group='auren_otools.group_extended_discount')

    group_extended_discount_1 = fields.Boolean(
        default=False, string="Activar descuento 1", config_parameter='auren_otools.group_extended_discount_1', implied_group='auren_otools.group_extended_discount_1')
    group_extended_discount_2 = fields.Boolean(
        default=False, string="Activar descuento 2", config_parameter='auren_otools.group_extended_discount_2', implied_group='auren_otools.group_extended_discount_2')
    group_extended_discount_3 = fields.Boolean(
        default=False, string="Activar descuento 3", config_parameter='auren_otools.group_extended_discount_3', implied_group='auren_otools.group_extended_discount_3')
    group_extended_discount_4 = fields.Boolean(
        default=False, string="Activar descuento 4", config_parameter='auren_otools.group_extended_discount_4', implied_group='auren_otools.group_extended_discount_4')
    group_extended_discount_5 = fields.Boolean(
        default=False, string="Activar descuento 5", config_parameter='auren_otools.group_extended_discount_5', implied_group='auren_otools.group_extended_discount_5')
    group_extended_discount_6 = fields.Boolean(
        default=False, string="Activar descuento 6", config_parameter='auren_otools.group_extended_discount_6', implied_group='auren_otools.group_extended_discount_6')

    desc_group_extended_discount_1 = fields.Char(
        default=False, string="Descripción descuento 1", config_parameter='auren_otools.desc_group_extended_discount_1')
    desc_group_extended_discount_2 = fields.Char(
        default=False, string="Descripción descuento 2", config_parameter='auren_otools.desc_group_extended_discount_2')
    desc_group_extended_discount_3 = fields.Char(
        default=False, string="Descripción descuento 3", config_parameter='auren_otools.desc_group_extended_discount_3')
    desc_group_extended_discount_4 = fields.Char(
        default=False, string="Descripción descuento 4", config_parameter='auren_otools.desc_group_extended_discount_4')
    desc_group_extended_discount_5 = fields.Char(
        default=False, string="Descripción descuento 5", config_parameter='auren_otools.desc_group_extended_discount_5')
    desc_group_extended_discount_6 = fields.Char(
        default=False, string="Descripción descuento 6", config_parameter='auren_otools.desc_group_extended_discount_6')

    operation_discount_1 = fields.Selection(required=True, string="Operación descuento 1", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_discount_1')

    operation_discount_2 = fields.Selection(required=True, string="Operación descuento 2", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_discount_2')

    operation_discount_3 = fields.Selection(required=True, string="Operación descuento 3", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_discount_3')

    operation_discount_4 = fields.Selection(required=True, string="Operación descuento 4", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_discount_4')

    operation_discount_5 = fields.Selection(required=True, string="Operación descuento 5", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_discount_5')

    operation_discount_6 = fields.Selection(required=True, string="Operación descuento 6", selection=[
        ('inc', 'Incrementa'),
        ('dec', 'Decrementa'),
    ], default="dec", config_parameter='auren_otools.operation_discount_6')

    type_discount = fields.Selection(required=True, string="Tipo", selection=[
        ('sum', 'Sumado'),
        ('app', 'Apilado'),
    ], default="app", config_parameter='auren_otools.type_discount')


# Ampliación de descuentos cabecera
    group_head_extended_discount = fields.Boolean(
        default=False, string="Descuento de venta ampliado cabecera", config_parameter='auren_otools.group_head_extended_discount', implied_group='auren_otools.group_head_extended_discount')

    add_vat_line_discount = fields.Boolean(string="Añadir Vat línea de descuento",
                                           config_parameter='auren_otools.add_vat_line_discount')

    group_head_extended_discount_1 = fields.Boolean(
        default=False, string="Activar head descuento 1", config_parameter='auren_otools.group_head_extended_discount_1', implied_group='auren_otools.group_head_extended_discount_1')
    group_head_extended_discount_2 = fields.Boolean(
        default=False, string="Activar head descuento 2", config_parameter='auren_otools.group_head_extended_discount_2', implied_group='auren_otools.group_head_extended_discount_2')
    group_head_extended_discount_3 = fields.Boolean(
        default=False, string="Activar head descuento 3", config_parameter='auren_otools.group_head_extended_discount_3', implied_group='auren_otools.group_head_extended_discount_3')
    group_head_extended_discount_4 = fields.Boolean(
        default=False, string="Activar head descuento 4", config_parameter='auren_otools.group_head_extended_discount_4', implied_group='auren_otools.group_head_extended_discount_4')
    group_head_extended_discount_5 = fields.Boolean(
        default=False, string="Activar head descuento 5", config_parameter='auren_otools.group_head_extended_discount_5', implied_group='auren_otools.group_head_extended_discount_5')
    group_head_extended_discount_6 = fields.Boolean(
        default=False, string="Activar head descuento 6", config_parameter='auren_otools.group_head_extended_discount_6', implied_group='auren_otools.group_head_extended_discount_6')

    product_discount_1_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='auren_otools.product_discount_1_id')
    product_discount_2_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='auren_otools.product_discount_2_id')
    product_discount_3_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='auren_otools.product_discount_3_id')
    product_discount_4_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='auren_otools.product_discount_4_id')
    product_discount_5_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='auren_otools.product_discount_5_id')
    product_discount_6_id = fields.Many2one("product.product",
                                            domain="[('type', '=', 'service')]", config_parameter='auren_otools.product_discount_6_id')

    desc_group_head_extended_discount_1 = fields.Char(
        default=False, string="Descripción descuento 1", config_parameter='auren_otools.desc_group_head_extended_discount_1')
    desc_group_head_extended_discount_2 = fields.Char(
        default=False, string="Descripción descuento 2", config_parameter='auren_otools.desc_group_head_extended_discount_2')
    desc_group_head_extended_discount_3 = fields.Char(
        default=False, string="Descripción descuento 3", config_parameter='auren_otools.desc_group_head_extended_discount_3')
    desc_group_head_extended_discount_4 = fields.Char(
        default=False, string="Descripción descuento 4", config_parameter='auren_otools.desc_group_head_extended_discount_4')
    desc_group_head_extended_discount_5 = fields.Char(
        default=False, string="Descripción descuento 5", config_parameter='auren_otools.desc_group_head_extended_discount_5')
    desc_group_head_extended_discount_6 = fields.Char(
        default=False, string="Descripción descuento 6", config_parameter='auren_otools.desc_group_head_extended_discount_6')

    operation_head_discount1 = fields.Selection(required=True, string="Operación descuento 1", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_head_discount1')

    operation_head_discount2 = fields.Selection(required=True, string="Operación descuento 2", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_head_discount2')

    operation_head_discount3 = fields.Selection(required=True, string="Operación descuento 3", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_head_discount3')

    operation_head_discount4 = fields.Selection(required=True, string="Operación descuento 4", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_head_discount4')

    operation_head_discount5 = fields.Selection(required=True, string="Operación descuento 5", selection=[
        ('inc', 'Incremente'),
        ('dec', 'Descrementa'),
    ], default="dec", config_parameter='auren_otools.operation_head_discount5')

    operation_head_discount6 = fields.Selection(required=True, string="Operación descuento 6", selection=[
        ('inc', 'Incrementa'),
        ('dec', 'Decrementa'),
    ], default="dec", config_parameter='auren_otools.operation_head_discount6')

    group_picking = fields.Boolean(
        default=False, string="Picking ampliado", config_parameter='auren_otools.group_picking', implied_group='auren_otools.group_picking')

    extended_ean_product = fields.Boolean(
        string="Gestión EAN automático",
        related='company_id.extended_ean_product',
        readonly=False,
        check_company=True,
    )
    extended_ean_product_country = fields.Char(string="Código pais",
                                               related='company_id.extended_ean_product_country',
                                               readonly=False,
                                               check_company=True,
                                               )
    extended_ean_product_company = fields.Char(string="Código Fabricante",
                                               related='company_id.extended_ean_product_company',
                                               readonly=False,
                                               check_company=True,
                                               )
    extended_ean_product_counter = fields.Integer(string="Contador",
                                                  related='company_id.extended_ean_product_counter',
                                                  readonly=False,
                                                  check_company=True,
                                                  )

    group_cost_standard = fields.Boolean(
        default=False, string="Cost standard", config_parameter='auren_otools.group_cost_standard', implied_group='auren_otools.group_cost_standard')

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

    @api.onchange('group_dim_inv')
    def _change_group_dim_inv(self):
        for conf in self:
            if (conf.group_dim_inv == False):
                conf.group_dim_sales = False
                conf.group_dim_purchase = False
                conf.group_dim_var1 = False
                conf.group_dim_var2 = False
                conf.group_dim_var3 = False
                conf.var1_s = False
                conf.var2_s = False
                conf.var3_s = False

    @api.onchange('var1_s', 'var2_s', 'var3_s')
    def _change_var_sales_var(self):
        for conf in self:
            if (conf.var1_s == False):
                conf.group_dim_var1 = False
            else:
                conf.group_dim_var1 = True
            if (conf.var2_s == False):
                conf.group_dim_var2 = False
            else:
                conf.group_dim_var2 = True
            if (conf.var3_s == False):
                conf.group_dim_var3 = False
            else:
                conf.group_dim_var3 = True
            conf._change_sales_var()
            conf._change_purchase_var()

    @api.onchange('group_dim_sales')
    def _change_sales_var(self):
        for conf in self:
            if (conf.group_dim_sales == False):
                conf.group_dim_var1_sales = False
                conf.group_dim_var2_sales = False
                conf.group_dim_var3_sales = False
            else:
                conf.group_dim_var1_sales = conf.group_dim_var1
                conf.group_dim_var2_sales = conf.group_dim_var2
                conf.group_dim_var3_sales = conf.group_dim_var3

    @api.onchange('group_dim_purchase')
    def _change_purchase_var(self):
        for conf in self:
            if (conf.group_dim_purchase == False):
                conf.group_dim_var1_purchase = False
                conf.group_dim_var2_purchase = False
                conf.group_dim_var3_purchase = False
            else:
                conf.group_dim_var1_purchase = conf.group_dim_var1
                conf.group_dim_var2_purchase = conf.group_dim_var2
                conf.group_dim_var3_purchase = conf.group_dim_var3

    @api.onchange('group_extended_uom_sale')
    def _change_uom_sale(self):
        for conf in self:
            if (conf.group_extended_uom_sale == False):
                conf.group_extended_uom_sale_qty = False
                conf.group_extended_uom_sale_con = False

    @api.onchange('group_extended_uom_purchase')
    def _change_uom_purchase(self):
        for conf in self:
            if (conf.group_extended_uom_purchase == False):
                conf.group_extended_uom_purchase_qty = False
                conf.group_extended_uom_purchase_con = False
