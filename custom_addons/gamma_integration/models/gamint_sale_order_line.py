from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # gi_stock_gamma = fields.Float(
    #     string="Stock Gamma", default=0.0, store=False)

    gi_stock_color = fields.Html(
        string="Stock G.")

    gi_producto_gamma = fields.Boolean(
        compute='_compute_gamma_product',
    )

    gi_last_date = fields.Datetime()
    gi_last_date_now = fields.Datetime(compute='_compute_date_time_now',)

    def _compute_date_time_now(self):
        self.gi_last_date_now = fields.Datetime.now().replace(second=0, microsecond=0)

    def _compute_gamma_product(self):
        for line in self:
            line.gi_producto_gamma = line.product_id.product_tmpl_id.gi_show_gamma_stock

    def action_get_stock(self):
        for line in self:
            product = line.product_id

            # Verificar si el producto tiene marcado el campo gi_show_gamma_stock
            if not product or not product.product_tmpl_id.gi_show_gamma_stock:
                raise UserError(
                    "Este producto no tiene habilitada la opción de obtener stock Gamma.")

            # Llama a la API y obtiene el stock actual del producto
            wizard = self.env['gamma.stock.wizard'].create({})
            stock_data = wizard.getstockbyitem(product)
            # Ajusta según el formato de respuesta de tu API
            stock_qty = stock_data.get('Qty', 0.0)

            qty_needed = line.product_uom_qty

            if stock_qty < qty_needed:
                color = "red"
                text = f"{stock_qty}"
            elif stock_qty == qty_needed:
                color = "orange"
                text = f"{stock_qty}"
            else:
                color = "green"
                text = f"{stock_qty}"

            line.gi_stock_color = f'<span style="color: {color}; font-weight: bold;">{text}</span>'
            line.gi_last_date = fields.Datetime.now().replace(second=0, microsecond=0)
