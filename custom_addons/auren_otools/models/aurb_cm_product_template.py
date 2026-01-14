from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmProductTemplate(models.Model):
    _inherit = "product.template"

    uom_sale_factor_ids = fields.One2many(
        "aurb.cm.product.uom.sale", 'product_id')
    uom_purchase_factor_ids = fields.One2many(
        "aurb.cm.product.uom.purchase", 'product_id')

    var1_s = fields.Float(string="var1")
    var2_s = fields.Float(string="var2")
    var3_s = fields.Float(string="var3")

    # var1_p = fields.Float(string="var1")
    # var2_p = fields.Float(string="var2")
    # var3_p = fields.Float(string="var3")

    uom_sale_id = fields.Many2one("uom.uom",
                                  help="Default unit of measure used for sale orders. It must be in the same category as the default unit of measure.")

    auren_property_cost_method = fields.Selection([
        ('standard', 'Standard Price'),
        ('fifo', 'First In First Out (FIFO)'),
        ('average', 'Average Cost (AVCO)')], compute='_compute_cost_method', string="Costing Method",
    )

    def _compute_cost_method(self):
        self.auren_property_cost_method = self.categ_id.property_cost_method

    cost_standards_ids = fields.One2many(
        "aurb.cm.cost.standard.item", 'product_id')

    @api.onchange('cost_standards_ids')
    def change_cost(self):

        for item in self:
            price = 0
            for cost in item.cost_standards_ids:
                price += cost.cost
            if (price != 0):
                item.standard_price = price

    @api.onchange('uom_sale_id')
    def _onchange_uom(self):
        if self.uom_sale_id and self.uom_id and self.uom_sale_id.category_id != self.uom_id.category_id:
            self.uom_sale_id = self.uom_id

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            # Compras

            # Ventas

            name_var1_s = parameters.get_param(
                'auren_otools.var1_s')
            name_var2_s = parameters.get_param(
                'auren_otools.var2_s')
            name_var3_s = parameters.get_param(
                'auren_otools.var3_s')
            if (name_var1_s != False):
                for node in arch.xpath(
                    "//field[@name='var1_s']"
                ):
                    node.attrib['string'] = name_var1_s
            if (name_var2_s != False):
                for node in arch.xpath(
                    "//field[@name='var2_s']"
                ):
                    node.attrib['string'] = name_var2_s
            if (name_var3_s != False):
                for node in arch.xpath(
                    "//field[@name='var3_s']"
                ):
                    node.attrib['string'] = name_var3_s

        return arch, view

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(AurbCmProductTemplate, self).create(vals_list)
        for product in templates:
            if (product.barcode == False):
                if (self.env.company.extended_ean_product):
                    code_country = self.env.company.extended_ean_product_country
                    code_company = self.env.company.extended_ean_product_company
                    code_number = self.env.company.extended_ean_product_counter
                    agrup_cat = False
                    if (product.categ_id):
                        if (product.categ_id.extended_ean_product):
                            code_number = product.categ_id.extended_ean_product_counter
                            agrup_cat = True
                    if (code_country and code_company and code_number):
                        code_number_string = str(code_number).zfill(5)
                        code_bar = code_country+code_company+code_number_string
                        digit_control = self.calcular_digito_control(code_bar)
                        product.barcode = code_bar+str(digit_control)
                        if (agrup_cat):
                            product.categ_id.extended_ean_product_counter = code_number+1
                        else:
                            self.env.company.extended_ean_product_counter = code_number+1
        return templates

    def calcular_digito_control(self, ean):
        if len(ean) != 12:
            raise ValueError("El EAN debe tener 12 dígitos.")

        suma_impares = sum(int(ean[i]) for i in range(0, 12, 2))
        suma_pares = sum(int(ean[i]) for i in range(1, 12, 2)) * 3

        suma_total = suma_impares + suma_pares
        digito_control = (10 - (suma_total % 10)) % 10

        return digito_control
