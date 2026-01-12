from odoo import models, fields, api
from odoo.exceptions import UserError
from .gamint_gamma_api import GammaAPI
from datetime import datetime

class ResCompany(models.Model):
    _inherit = 'res.company'

    def update_supplier_prices(self):
        """Actualiza o crea precios del proveedor Gamma en product.supplierinfo."""
        # Comprueba que la compañía actual (self) tiene configurado el proveedor Gamma en el campo gi_supplier
        self.ensure_one()
        if not self.gi_supplier:
            raise UserError("Debe configurar el proveedor Gamma en los ajustes.")

        # Conexión con la API Gamma
        # Crea una instancia de GammaAPI pasando la compañía actual
        gamma = GammaAPI(self)
        # Llama al método get_prices() para descargar la lista de precios desde el webservice Gamma
        # El resultado es una lista de diccionarios, cada uno con información de un 
        # artículo (código, descripción, tarifas, precios, cantidades, fecha de aplicación)
        price_data = gamma.get_prices()
        supplier_id = self.gi_supplier.id

        # Obtener los tipos de precio que existen en Odoo
        # Solo se procesarán las tarifas para estos tipos
        existing_price_types = self.env['gi.type.price'].search([]).mapped('code')

        # Iteración sobre los datos recibidos
        # Para cada artículo (item) en la lista extrae los datos clave
        for item in price_data:
            cod_articulo = item.get("COD_ARTICULO")             # código del artículo Gamma
            
            # FILTRO TEMPORAL: solo procesar el artículo CEYCA002
            # if cod_articulo != "CEYCA002":
            #     continue
            
            descripcion = item.get("DESCRIPCION")               # descripción del artículo
            codigo_tarifa = item.get("COD_TARIFA_AGRUPADA")     # código de la tarifa
            descripcion_tarifa = item.get("DESCRIPCION_TARIFA") # descripción de la tarifa
            fecha_aplicacion_raw = item.get("FECHA_APLICACION") # fecha de aplicación en formato "YYYYMMDD" (se conviderte a YYYY-MM-DD)
            fecha_aplicacion = False
            if fecha_aplicacion_raw:
                try:
                    fecha_aplicacion = datetime.strptime(fecha_aplicacion_raw, "%Y%m%d").date()
                except ValueError:
                    fecha_aplicacion = False    # Si falla, no asignamos fecha

            # Buscar producto por gi_code_gamma
            # Busca el product.template cuyo campo gi_code_gamma coincida con COD_ARTICULO
            product = self.env['product.template'].search([('gi_code_gamma', '=', cod_articulo)], limit=1)
            # Si no encuentra el producto, salta al siguiente artículo
            if not product:
                continue

            # Actualiza el campo gi_desc del producto con la descripción Gamma (DESCRIPCION)
            product.gi_desc = descripcion

            # Procesar precios por tipo (U, C, P)
            # Define una lista con los tres tipos de precio
            precios = [
                ('U', item.get("PVP_UNIDAD"), item.get("UNIDADES")),
                ('C', item.get("PVP_CANTIDAD"), item.get("UNIDADES_CANTIDAD")),
                ('P', item.get("PVP_PALET"), item.get("UNIDADES_PALET")),
            ]

            # Para cada tipo
            for tipo, precio, min_qty in precios:
                # Solo procesar si el tipo de precio existe en Odoo
                if tipo not in existing_price_types:
                    continue

                # Si el precio es mayor que 0, procede a crear o actualizar el registro en product.supplierinfo
                if precio and precio > 0:
                    # Busca en product.supplierinfo un registro que coincida con:
                    # product_tmpl_id = ID del producto
                    # partner_id = ID del proveedor Gamma
                    # gi_type.code = tipo (U, C o P)
                    supplierinfo = self.env['product.supplierinfo'].search([
                        ('product_tmpl_id', '=', product.id),
                        ('partner_id', '=', supplier_id),
                        ('gi_type.code', '=', tipo)
                    ], limit=1)

                    # Prepara un diccionario vals con los valores a actualizar o crear
                    vals = {
                        'partner_id': supplier_id,
                        'product_tmpl_id': product.id,
                        'product_code': product.default_code,
                        'price': precio,
                        'min_qty': min_qty or 1,
                        'date_start': fecha_aplicacion,
                        'gi_code_tarf': codigo_tarifa,
                        'gi_name_tarf': descripcion_tarifa,
                        'gi_type': self.env['gi.type.price'].search([('code', '=', tipo)], limit=1).id
                    }

                    # Si el registro existe → lo actualiza (write)
                    if supplierinfo:
                        supplierinfo.write(vals)
                    # Si no existe → lo crea (create)
                    else:
                        self.env['product.supplierinfo'].create(vals)