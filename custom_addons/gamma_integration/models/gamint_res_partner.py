from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_gamma_supplier = fields.Boolean(compute="_compute_is_gamma_supplier")

    def action_get_gamma_prices(self):
        """Botón manual para actualizar precios Gamma desde la ficha del proveedor."""
        self.ensure_one()
        company = self.env.company
        if self.id != company.gi_supplier.id:
            raise UserError("Este proveedor no está configurado como proveedor Gamma.")
        company.update_supplier_prices()
        
        # Mostrar mensaje al usuario
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Proceso completado',
                'message': 'El proceso ha finalizado correctamente.',
                'type': 'success',  # success, warning, danger
                'sticky': False,    # True para que no se cierre automáticamente
            }
        }

        
    def _compute_is_gamma_supplier(self):
        company = self.env.company
        for partner in self:
            partner.is_gamma_supplier = (partner.id == company.gi_supplier.id)
