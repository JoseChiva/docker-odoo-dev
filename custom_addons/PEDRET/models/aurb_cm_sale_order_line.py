from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class AurbCmSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    pick_order = fields.Integer(string="Order")
    pick_comment = fields.Char(string="Comentario")
    pick_print = fields.Boolean(default=True, string="Imprimir")
    pick_delivery = fields.Boolean(default=False, string="Entregado")
    pick_travel_num = fields.Integer()

    pick_pro_order = fields.Char(string="Número")

    pick_id = fields.One2many('aurb.sale.picking', 'sale_order_line_ids')

    res_partner_contact = fields.Many2one("res.partner", string="Persona de contacto",
                                          domain="[('is_company','=',False),('type','=','contact')]", compute="_compute_contact_person")

    pick_date_ship = fields.Date(
        'Fecha', default=fields.Date.today() + relativedelta(days=1), required=True)

    price_with_var1 = fields.Float()
    price_with_var2 = fields.Float()
    price_with_var3 = fields.Float()

    num_contract = fields.Char()

    price_base = fields.Float(string="Precio base")
    add_price_unit = fields.Float(string="Inc. unit.")

    @api.onchange('add_price_unit')
    def change_add_price_unit(self):
        if (self.add_price_unit):
            if (self.price_base):
                if (self.product_uom_qty):
                    self.price_unit = self.price_base + \
                        (self.add_price_unit)

    @api.model
    def create(self, vals):
        result = super().create(vals)
        for lin in result:
            self.price_base = self.price_unit
        return result

    def _compute_contact_person(self):
        for line in self:
            line.res_partner_contact = False
            if (line.order_id):
                if (line.order_id):
                    line.res_partner_contact = line.order_id.res_partner_contact

    def _get_pricelist_price(self):
        for line in self:
            resultado = super()._get_pricelist_price()
            if (line.pricelist_item_id.compute_price == 'fixed'):
                if (line.pricelist_item_id.price_with_var1):
                    line.price_with_var1 = line.pricelist_item_id.price_with_var1
                else:
                    line.price_with_var1 = 0
                if (line.pricelist_item_id.price_with_var2):
                    line.price_with_var2 = line.pricelist_item_id.price_with_var2
                else:
                    line.price_with_var2 = 0
                if (line.pricelist_item_id.price_with_var3):
                    line.price_with_var3 = line.pricelist_item_id.price_with_var3
                else:
                    line.price_with_var3 = 0
                if (line.pricelist_item_id.num_contract):
                    line.num_contract = line.pricelist_item_id.num_contract
                else:
                    line.num_contract = ''

                if (line.order_id.type_transport == "var1"):
                    if (line.pricelist_item_id.price_with_var1):
                        resultado = line.pricelist_item_id.price_with_var1
                elif (line.order_id.type_transport == "var2"):
                    if (line.pricelist_item_id.price_with_var2):
                        resultado = line.pricelist_item_id.price_with_var2
                elif (line.order_id.type_transport == "var3"):
                    if (line.pricelist_item_id.price_with_var3):
                        resultado = line.pricelist_item_id.price_with_var3
            else:
                line.price_with_var1 = 0
                line.price_with_var2 = 0
                line.price_with_var3 = 0
                line.num_contract = ''
        line.price_base = resultado
        if (line.add_price_unit):
            resultado += (line.add_price_unit)

        return resultado
