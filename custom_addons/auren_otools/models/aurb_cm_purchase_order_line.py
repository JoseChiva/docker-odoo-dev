from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    unit = fields.Float(string="Unidades")
    var1 = fields.Float(string="var1")
    var2 = fields.Float(string="var2")

    var3 = fields.Float(string="var3")

    qty_inventory = fields.Float(
        string="Quantity Inventory", default=1, digits=(12, 5))

    conversion_factor = fields.Float(
        string="conversion_factor", default=1, digits=(12, 8))
    unit__factor = fields.Float(
        string="unit__factor", default=1, digits=(12, 8))

    formula = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3"
    )

    @api.onchange('product_id')
    def getvarproduct(self):
        parameters = self.env['ir.config_parameter'].sudo()

        group_dim_purchase = self.env.user.has_group(
            'auren_otools.group_dim_purchase')

        if (group_dim_purchase):
            for record in self:
                var1 = record.product_id.var1_s
                var2 = record.product_id.var2_s
                var3 = record.product_id.var3_s
                if (var1):
                    record.var1 = var1
                if (var2):
                    record.var2 = var2
                if (var3):
                    record.var3 = var3

    @api.onchange('var1', 'var2', 'var3', 'product_uom', 'unit')
    def _calculation(self):
        parameters = self.env['ir.config_parameter'].sudo()

        group_dim_purchase = self.env.user.has_group(
            'auren_otools.group_dim_purchase')

        formula_s = parameters.get_param(
            'auren_otools.formula_s')
        formula_s_2 = parameters.get_param(
            'auren_otools.formula_s_2')
        formula_s_3 = parameters.get_param(
            'auren_otools.formula_s_3')
        formula_s_4 = parameters.get_param(
            'auren_otools.formula_s_4')

        inventory_uom_expanded = self.env.user.has_group(
            'auren_otools.group_extended_uom_purchase')

        if (inventory_uom_expanded):
            for record in self:

                product_id = record.product_id.product_tmpl_id.id
                product_uom_sales = record.product_uom.id
                product_uom_inventory = record.product_id.product_tmpl_id.uom_id.id

                record.conversion_factor, record.unit__factor, record.formula = get_factor_sale(product_id, product_uom_sales, product_uom_inventory,
                                                                                                self
                                                                                                )
        if (group_dim_purchase):
            for record in self:
                uom_sale = parameters.get_param('auren_otools.uom_sale')
                uom_sale_2 = parameters.get_param('auren_otools.uom_sale_2')
                uom_sale_3 = parameters.get_param('auren_otools.uom_sale_3')
                uom_sale_4 = parameters.get_param('auren_otools.uom_sale_4')

                if (uom_sale):
                    uom_sale = int(uom_sale)
                if (uom_sale_2):
                    uom_sale_2 = int(uom_sale_2)
                if (uom_sale_3):
                    uom_sale_3 = int(uom_sale_3)
                if (uom_sale_4):
                    uom_sale_4 = int(uom_sale_4)

                product_uom_sales = record.product_uom.id

                same_uom = False

                if (record.formula == False and uom_sale == product_uom_sales):
                    record.formula = formula_s
                    same_uom = True
                if (record.formula == False and uom_sale_2 == product_uom_sales):
                    record.formula = formula_s_2
                    same_uom = True
                if (record.formula == False and uom_sale_3 == product_uom_sales):
                    record.formula = formula_s_3
                    same_uom = True
                if (record.formula == False and uom_sale_4 == product_uom_sales):
                    record.formula = formula_s_4
                    same_uom = True

                if (same_uom):
                    if (record.var3 == False):
                        if (record.var2 == False):
                            if (record.var1):
                                formula = record.formula
                                record.formula = record.formula.replace(
                                    "var1", str(record.var1))
                                record.formula = record.formula.replace(
                                    "var2", str(1))
                                record.formula = record.formula.replace(
                                    "var3", str(1))
                                try:
                                    record.product_qty = record.unit * \
                                        eval(record.formula)
                                except:
                                    raise ValidationError(
                                        "Fórmula incorrecta : {form}".format(form=formula))
                            else:
                                if (record.unit):
                                    record.product_qty = record.unit
                        else:
                            if (record.var1 and record.var2):
                                formula = record.formula
                                record.formula = record.formula.replace(
                                    "var1", str(record.var1))
                                record.formula = record.formula.replace(
                                    "var2", str(record.var2))
                                record.formula = record.formula.replace(
                                    "var3", str(1))
                                try:
                                    record.product_qty = record.unit * \
                                        eval(record.formula)
                                except:
                                    raise ValidationError(
                                        "Fórmula incorrecta : {form}".format(form=formula))
                            else:
                                if (record.unit):
                                    record.product_uom_qty = record.unit

                    else:
                        if (record.var1 and record.var2 and record.var3):
                            record.formula = record.formula.replace(
                                "var1", str(record.var1))
                            record.formula = record.formula.replace(
                                "var2", str(record.var2))
                            record.formula = record.formula.replace(
                                "var3", str(record.var3))
                            try:
                                record.product_qty = record.unit * \
                                    eval(record.formula)
                            except:
                                raise ValidationError(
                                    "Fórmula incorrecta : {form}".format(form=formula))
                        else:
                            if (record.unit):
                                record.product_uom_qty = record.unit
                else:
                    record.product_uom_qty = record.unit

        if (inventory_uom_expanded):
            for record in self:
                # record.conversion_factor = record.conversion_factor
                if (record.conversion_factor != False):
                    record.product_uom_qty = record.product_uom_qty*record.unit__factor
                    record.qty_inventory = record.product_uom_qty*record.conversion_factor
                else:
                    record.qty_inventory = record.product_uom_qty


def get_factor_sale(product_id, uom_sale, uom_inventory,  self):
    if (product_id != False):
        query = "SELECT conversion_factor,unit__factor,formula FROM aurb_cm_product_uom_purchase uom JOIN product_template pt on uom.product_id=pt.id WHERE uom.product_id={} and uom.uom_id={} and pt.uom_id={}".format(
            product_id, uom_sale, uom_inventory)
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        if len(result) > 0:
            for row in result:
                # return [row[0], row[1], row[2]]
                # Se quita la funcionalidad de fórmula a nivel de unidad de medida
                return [row[0], 1, False]
    return [False, 1,  False]
