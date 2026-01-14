from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmStockMove(models.Model):
    _inherit = "stock.move"

    conversion_factor = fields.Float(
        string="conversion_factor", default=1, digits=(12, 8))
    unit__factor = fields.Float(
        string="unit__factor", default=1, digits=(12, 8))

    formula = fields.Char(
        string="Fórmula", default="var1*var2*var3", help="Fórmula de calculo entre dimensiones Ejemplo : var1*var2/var3"
    )

    pick_order = fields.Integer(string="Order")
    pick_comment = fields.Char(string="Comentario")
    pick_print = fields.Boolean(default=True, string="Imprimir")
    pick_pro_order = fields.Char(string="Número")

    res_partner_contact = fields.Many2one("res.partner", string="Persona de contacto",
                                          domain="[('is_company','=',False),('type','=','contact')]", compute="_compute_contact_person")

    def _compute_contact_person(self):
        for line in self:
            line.res_partner_contact = False
            if (line.picking_id):
                if (line.picking_id.sale_id):
                    if (line.picking_id.sale_id.res_partner_contact):
                        line.res_partner_contact = line.picking_id.sale_id.res_partner_contact

    @api.model
    def create(self, vals):
        records = super().create(vals)

        for record in records:
            if (record.sale_line_id or record.purchase_line_id):
                parameters = self.env['ir.config_parameter'].sudo()
                inventory_uom_expanded = self.env.user.has_group(
                    get_parameters_inventory_uom_expanded(record))

                if (record.sale_line_id):
                    formula = parameters.get_param(
                        'auren_otools.formula_s')
                if (record.purchase_line_id):
                    formula = parameters.get_param(
                        'auren_otools.formula_p')

                if (inventory_uom_expanded):

                    if (record.sale_line_id or record.purchase_line_id):
                        product_id = record.product_tmpl_id.id
                        if (record.sale_line_id):
                            product_uom_sales = record.sale_line_id.product_uom.id
                        if (record.purchase_line_id):
                            product_uom_sales = record.purchase_line_id.product_uom.id

                        product_uom_inventory = record.product_uom.id
                        record.conversion_factor, record.unit__factor, record.formula = get_factor(
                            product_id, product_uom_sales, product_uom_inventory, self, record)

                if (inventory_uom_expanded):
                    if (record.sale_line_id or record.purchase_line_id):
                        if (record.conversion_factor != False):
                            if (record.sale_line_id):
                                sale_qty = record.sale_line_id.product_uom_qty
                            if (record.purchase_line_id):
                                sale_qty = record.purchase_line_id.product_qty
                            record.product_uom_qty = sale_qty*record.conversion_factor
        return records


def get_parameters_inventory_uom_expanded(record):
    if (record.sale_line_id):
        return 'auren_otools.group_extended_uom_sale'
    if (record.purchase_line_id):
        return 'auren_otools.group_extended_uom_purchase'


def get_factor(product_id, uom_sale, uom_inventory,  self, record):
    if (product_id != False):
        if (record.sale_line_id):
            query = "SELECT conversion_factor,unit__factor,formula FROM aurb_cm_product_uom_sale uom JOIN product_template pt on uom.product_id=pt.id WHERE uom.product_id={} and uom.uom_id={} and pt.uom_id={}".format(
                product_id, uom_sale, uom_inventory)
        if (record.purchase_line_id):
            query = "SELECT conversion_factor,unit__factor,formula FROM aurb_cm_product_uom_purchase uom JOIN product_template pt on uom.product_id=pt.id WHERE uom.product_id={} and uom.uom_id={} and pt.uom_id={}".format(
                product_id, uom_sale, uom_inventory)
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        if len(result) > 0:
            for row in result:
                # return [row[0], row[1], row[2]]
                # Se quita la funcionalidad de formula a nivel de unidad de medida
                return [row[0], 1, False]
    return [False, 1, False]
