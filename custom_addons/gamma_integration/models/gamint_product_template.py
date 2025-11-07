from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    gi_mang_gamma = fields.Boolean(
        string="Es producto Gamma",
        compute="_compute_gi_mang_gamma",
    )

    gi_code_gamma = fields.Char(
        string="Código Gamma",
        readonly=False,
        store=True,
    )

    gi_stock_gamma = fields.Float(
        string="Stock Gamma",
        store=True,
    )
    gi_show_gamma_stock = fields.Boolean(string="Mostrar stock Gamma", compute="_compute_show_gamma", store=True)

    # Marca automáticamente el campo gi_mang_gamma si el producto tiene la etiqueta configurada en gi_tag_gamma
    @api.depends('product_tag_ids')
    def _compute_gi_mang_gamma(self):
        param = self.env['ir.config_parameter'].sudo().get_param('gamma_integration.gi_tag_gamma')
        param = self.env.company.gi_tag_gamma.id
        try:
            tag_gamma_id = int(param) if param else None
        except ValueError:
            tag_gamma_id = None

        for product in self:
            if tag_gamma_id and tag_gamma_id in product.product_tag_ids.ids:
                product.gi_mang_gamma = True
            else:
                product.gi_mang_gamma = False

    # carga el código del artículo sobre el campo gi_code_gamma de forma automática al crear o modificar el producto
    # @api.model
    # def create(self, vals):
    #     if not vals.get('gi_code_gamma') and vals.get('default_code'):
    #         vals['gi_code_gamma'] = vals['default_code']
    #     return super(ProductTemplate, self).create(vals)

    # def write(self, vals):
    #     for product in self:
    #         if not vals.get('gi_code_gamma') and product.default_code:
    #             vals['gi_code_gamma'] = product.default_code
    #     return super(ProductTemplate, self).write(vals)
    
    # muestra u oculta el campo gi_stock_gamma y el botón en la vista según si el producto pertenece a la categoría/etiqueta configurada en gi_tag_gamma
    @api.depends('product_tag_ids')
    def _compute_show_gamma(self):
        tag = self.env.company.gi_tag_gamma
        for rec in self:
            rec.gi_show_gamma_stock = tag.id in rec.product_tag_ids.ids

    # Obtiene el stock actual desde Gamma para el/los producto(s) seleccionados y actualiza el campo gi_stock_gamma
    def action_get_stock(self):
        # Verificar si el producto tiene marcado el campo gi_show_gamma_stock
        if not self.gi_code_gamma or not self.gi_show_gamma_stock:
            raise UserError("Este producto no tiene habilitada la opción de obtener stock Gamma.")

        for product in self:
            self.env['gamma.stock.wizard'].getstockbyitem(product)