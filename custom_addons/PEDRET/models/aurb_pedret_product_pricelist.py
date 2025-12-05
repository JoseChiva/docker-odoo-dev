from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class AurbPedretProductPriceList(models.Model):
    _inherit = "product.pricelist"

    res_partner_id = fields.Many2one("res.partner", string="Obra")
    sale_order_ids = fields.Many2many("sale.order")

    @api.onchange('res_partner_id')
    def _change_res_partner_id(self):
        for pricelist in self:
            if (pricelist.res_partner_id):
                pricelist.res_partner_id.property_product_pricelist = self.id

    def button_create_sale_order(self):
        self.ensure_one()

        # Verificar que tenemos un partner asignado
        if not self.res_partner_id:
            raise UserError(
                _("Debe asignar una Obra (res_partner_id) antes de crear un pedido de venta."))

        # Crear el pedido de venta
        sale_order_vals = {
            'partner_id': self.res_partner_id.id,
            'pricelist_id': self.id,
            'date_order': fields.Datetime.now(),
        }

        sale_order = self.env['sale.order'].create(sale_order_vals)

        # Obtener las líneas del pricelist
        order_lines = []
        for item in self.item_ids:
            # Verificar que el item tiene un producto
            if item.product_tmpl_id or item.product_id:
                product_id = item.product_id or item.product_tmpl_id.product_variant_id

                # Crear valores para la línea de pedido
                order_line_vals = {
                    'order_id': sale_order.id,
                    'product_id': product_id.id,
                    'product_uom_qty': 1.0,
                    'price_unit': item.fixed_price,  # Usar el precio fijo del pricelist
                }
                order_lines.append((0, 0, order_line_vals))

        # Si no hay líneas, mostrar advertencia
        if not order_lines:
            raise UserError(
                _("No hay productos configurados en el pricelist para crear el pedido de venta."))

        # Añadir las líneas al pedido
        sale_order.write({'order_line': order_lines})

        # Añadir la referencia a sale_order_ids
        self.write({'sale_order_ids': [(4, sale_order.id)]})

        # Mensaje de confirmación
        message = _("Pedido de venta %s creado exitosamente") % sale_order.name
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
            'context': self._context,
        }
