# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AurenExUomResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    # Artículos
    group_dim_inv = fields.Boolean(
        default=False, string="Artículos con dimensiones", config_parameter='extended_uom.group_dim_inv', implied_group='extended_uom.group_dim_inv')

    group_dim_var1 = fields.Boolean(
        default=False, string="Gestión con dimensiones var1", config_parameter='extended_uom.group_dim_var1', implied_group='extended_uom.group_dim_var1')
    group_dim_var2 = fields.Boolean(
        default=False, string="Gestión con dimensiones var2", config_parameter='extended_uom.group_dim_var2', implied_group='extended_uom.group_dim_var2')
    group_dim_var3 = fields.Boolean(
        default=False, string="Gestión con dimensiones var3", config_parameter='extended_uom.group_dim_var3', implied_group='extended_uom.group_dim_var3')

    var1_s = fields.Char(string="Nombre dimensión 1",
                         config_parameter='extended_uom.var1_s')
    var2_s = fields.Char(string="Nombre dimensión 2",
                         config_parameter='extended_uom.var2_s')
    var3_s = fields.Char(string="Nombre dimensión 3",
                         config_parameter='extended_uom.var3_s')

    uom_sale = fields.Many2one("uom.uom",
                               help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='extended_uom.uom_sale'
                               )
    uom_sale_2 = fields.Many2one("uom.uom",
                                 help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='extended_uom.uom_sale_2'
                                 )

    uom_sale_3 = fields.Many2one("uom.uom",
                                 help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='extended_uom.uom_sale_3'
                                 )
    uom_sale_4 = fields.Many2one("uom.uom",
                                 help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.", config_parameter='extended_uom.uom_sale_4'
                                 )

    formula_s = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='extended_uom.formula_s'
    )
    formula_s_2 = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='extended_uom.formula_s_2'
    )

    formula_s_3 = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='extended_uom.formula_s_3'
    )
    formula_s_4 = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3", config_parameter='extended_uom.formula_s_4'
    )

    # Ventas

    group_dim_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones", config_parameter='extended_uom.group_dim_sales', implied_group='extended_uom.group_dim_sales')

    group_dim_var1_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones sales var1", config_parameter='extended_uom.group_dim_var1_sales', implied_group='extended_uom.group_dim_var1_sales')
    group_dim_var2_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones sales var2", config_parameter='extended_uom.group_dim_var2_sales', implied_group='extended_uom.group_dim_var2_sales')
    group_dim_var3_sales = fields.Boolean(
        default=False, string="Gestión con dimensiones sales var3", config_parameter='extended_uom.group_dim_var3_sales', implied_group='extended_uom.group_dim_var3_sales')

    var_readonly_s = fields.Boolean(
        default=False, string="Dimensiones sólo lectura", config_parameter='extended_uom.var_readonly_s')

    group_extended_uom_sale = fields.Boolean(
        default=False, string="Inventario Uom Ampliada", config_parameter='extended_uom.group_extended_uom_sale', implied_group='extended_uom.group_extended_uom_sale')

    group_extended_uom_sale_con = fields.Boolean(
        default=False, string="Visualzar Factor de Conversión en Documentos", config_parameter='extended_uom.group_extended_uom_sale_con', implied_group='extended_uom.group_extended_uom_sale_con')
    group_extended_uom_sale_qty = fields.Boolean(
        default=False, string="Visualizar Cantidad UoM en Documentos", config_parameter='extended_uom.group_extended_uom_sale_qty', implied_group='extended_uom.group_extended_uom_sale_qty')

    # Compras

    group_dim_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones", config_parameter='extended_uom.group_dim_purchase', implied_group='extended_uom.group_dim_purchase')

    group_dim_var1_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones purchase var1", config_parameter='extended_uom.group_dim_var1_purchase', implied_group='extended_uom.group_dim_var1_purchase')
    group_dim_var2_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones purchase var2", config_parameter='extended_uom.group_dim_var2_purchase', implied_group='extended_uom.group_dim_var2_purchase')
    group_dim_var3_purchase = fields.Boolean(
        default=False, string="Gestión con dimensiones purchase var3", config_parameter='extended_uom.group_dim_var3_purchase', implied_group='extended_uom.group_dim_var3_purchase')

    var_readonly_p = fields.Boolean(
        default=False, string="Dimensiones sólo lectura", config_parameter='extended_uom.var_readonly_p')

    group_extended_uom_purchase = fields.Boolean(
        default=False, string="Inventario Uom Ampliada", config_parameter='extended_uom.group_extended_uom_purchase', implied_group='extended_uom.group_extended_uom_purchase')

    group_extended_uom_purchase_con = fields.Boolean(
        default=False, string="Visualzar Factor de Conversión en Documentos", config_parameter='extended_uom.group_extended_uom_purchase_con', implied_group='extended_uom.group_extended_uom_purchase_con')
    group_extended_uom_purchase_qty = fields.Boolean(
        default=False, string="Visualizar Cantidad UoM en Documentos", config_parameter='extended_uom.group_extended_uom_purchase_qty', implied_group='extended_uom.group_extended_uom_purchase_qty')

    group_extended_uom_scandal = fields.Boolean(
        default=False, string="Escandallo Uom Ampliada", config_parameter='extended_uom.group_extended_uom_scandal', implied_group='extended_uom.group_extended_uom_scandal')

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
