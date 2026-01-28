from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _
import logging

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class SucoPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    price_base = fields.Float(string="Precio base")
    add_price_unit = fields.Float(string="Inc. unit.")

    @api.onchange('add_price_unit')
    def change_add_price_unit(self):
        if (self.add_price_unit):
            if (self.price_base):
                if (self.product_qty):
                    self.price_unit = self.price_base + \
                        (self.add_price_unit)

    def _compute_price_unit_and_date_planned_and_name(self):
        super()._compute_price_unit_and_date_planned_and_name()
        for line in self:
            line.price_base = line.price_unit
            if (line.price_base):
                line.price_unit = line.price_base + \
                    (line.add_price_unit)

    @api.onchange('product_id')
    def _onchange_product_id_packaging_default(self):
        """Establecer embalaje por defecto cuando se selecciona un producto"""
        _logger.info("=" * 80)
        _logger.info("INICIO _onchange_product_id_packaging_default - product_id: %s", self.product_id.name if self.product_id else None)
        
        result = {}
        if self.product_id and self.product_id.packaging_ids:
            packaging = self.product_id.packaging_ids[0]
            _logger.info("Embalaje encontrado: %s (qty: %s)", packaging.name, packaging.qty)
            
            # Asegurarse de que product_uom esté establecido (del producto)
            if not self.product_uom:
                self.product_uom = self.product_id.uom_po_id
                _logger.info("Establecido product_uom: %s", self.product_uom.name)
            
            # Establecer el embalaje y la cantidad de embalaje
            self.product_packaging_id = packaging.id
            _logger.info("Establecido product_packaging_id: %s", packaging.name)
            
            self.product_packaging_qty = 1.0
            _logger.info("Establecido product_packaging_qty: %s", self.product_packaging_qty)
            
            # FORZAR product_qty = packaging_qty * packaging.qty
            self.product_qty = self.product_packaging_qty * packaging.qty
            _logger.info("FORZADO product_qty: %s", self.product_qty)
            
            # Retornar warning vacío para evitar que Odoo aplique su validación
            result = {'warning': {}}
            
        _logger.info("FIN _onchange_product_id_packaging_default - qty=%s, pkg_qty=%s, pkg_id=%s, uom=%s",
                    self.product_qty, self.product_packaging_qty, 
                    self.product_packaging_id.name if self.product_packaging_id else None,
                    self.product_uom.name if self.product_uom else None)
        _logger.info("=" * 80)
        return result
    
    @api.onchange('product_qty', 'product_uom')
    def _onchange_product_qty_custom(self):
        """Calcular product_packaging_qty cuando cambia product_qty manualmente"""
        _logger.info("-" * 80)
        _logger.info("INICIO _onchange_product_qty_custom")
        _logger.info("product_qty: %s, product_packaging_qty: %s", self.product_qty, self.product_packaging_qty)
        
        # Si hay embalaje, calcular product_packaging_qty
        if self.product_packaging_id and self.product_packaging_id.qty and self.product_qty:
            old_pkg_qty = self.product_packaging_qty
            self.product_packaging_qty = self.product_qty / self.product_packaging_id.qty
            _logger.info("Recalculado product_packaging_qty: %s -> %s", old_pkg_qty, self.product_packaging_qty)
        
        _logger.info("FIN _onchange_product_qty_custom")
        _logger.info("-" * 80)
            
    @api.onchange('product_packaging_id', 'product_packaging_qty')
    def _onchange_product_packaging_purchase(self):
        """Calcular product_qty basado en product_packaging_qty"""
        _logger.info("*" * 80)
        _logger.info("INICIO _onchange_product_packaging_purchase")
        _logger.info("product_qty: %s, product_packaging_qty: %s, product_packaging_id: %s",
                    self.product_qty, self.product_packaging_qty,
                    self.product_packaging_id.name if self.product_packaging_id else None)
        
        # SIEMPRE calcular product_qty basado en product_packaging_qty
        if self.product_packaging_id and self.product_packaging_qty:
            old_qty = self.product_qty
            self.product_qty = self.product_packaging_qty * self.product_packaging_id.qty
            _logger.info("Calculado product_qty: %s -> %s", old_qty, self.product_qty)
        
        _logger.info("FIN _onchange_product_packaging_purchase")
        _logger.info("*" * 80)
        
        # Retornar warning vacío para suprimir el warning de packaging de Odoo
        return {'warning': {}}

