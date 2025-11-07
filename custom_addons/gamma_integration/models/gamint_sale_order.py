from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_get_stock_all_lines(self):
        for order in self:
            # Verificar si el pedido tiene líneas
            for line in order.order_line:
                # Verificar si la línea tiene un producto asociado
                product = line.product_id
                # Verificar si el producto tiene marcado el campo gi_show_gamma_stock
                if not product or not product.product_tmpl_id.gi_show_gamma_stock:
                    line.gi_stock_color = ''
                    continue
                # Verificar si el producto tiene un código gamma
                gamma_code = product.product_tmpl_id.gi_code_gamma
                if not gamma_code:
                    line.gi_stock_color = ''
                    continue

                # Llama a la API y obtiene el stock actual del producto
                wizard = self.env['gamma.stock.wizard'].create({})
                stock_data = wizard.getstockbyitem(product)
                stock_qty = stock_data.get('Qty', 0.0)
                qty_needed = line.product_uom_qty

                # Determina el color y el texto según la cantidad de stock
                if stock_qty < qty_needed:
                    color = "red"
                    text = f"{stock_qty}"
                elif stock_qty == qty_needed:
                    color = "orange"
                    text = f"{stock_qty}"
                else:
                    color = "green"
                    text = f"{stock_qty}"

                # Actualiza el campo gi_stock_color con el color y el texto
                line.gi_stock_color = f'<span style="color: {color}; font-weight: bold;">{text}</span>'
                line.gi_last_date = fields.Datetime.now().replace(second=0, microsecond=0)
