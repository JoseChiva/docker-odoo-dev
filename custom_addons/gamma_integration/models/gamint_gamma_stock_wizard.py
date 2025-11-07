from odoo import models
from .gamint_gamma_api import GammaAPI

class GammaStockWizard(models.TransientModel):
    _name = 'gamma.stock.wizard'
    _description = 'Obtener stock desde Gamma'

    def getstock(self):
        company = self.env.company
        gamma = GammaAPI(company)
        stock_data = gamma.get_stock()

        # Solo trabajar con productos cuyo template tenga gi_show_gamma_stock=True
        products_to_update = self.env['product.product'].search([
            ('product_tmpl_id.gi_show_gamma_stock', '=', True),
            ('product_tmpl_id.gi_code_gamma', '!=', False)
        ])

        # Crear un diccionario para búsquedas más rápidas
        products_to_update_dict = {p.default_code: p for p in products_to_update}

        for item_code, item_info in stock_data.items():
            product = products_to_update_dict.get(item_code)
            if product:
                product.gi_stock_gamma = item_info.get('Qty', 0.0)

    def getstockbyitem(self, product):
        company = self.env.company
        gamma = GammaAPI(company)
        stock_data = gamma.get_stock_by_item(product.product_tmpl_id.gi_code_gamma)
        # Si la API no devuelve nada, retorna un diccionario vacío
        return stock_data or {}