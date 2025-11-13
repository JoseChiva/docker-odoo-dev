import requests
from datetime import datetime, timedelta
import pytz
from odoo import models
from odoo.exceptions import UserError
import logging
from email.utils import parsedate_to_datetime

import gzip
import io
import json

_logger = logging.getLogger(__name__)

class GammaAPI:
    def __init__(self, company):
        # Inicializa una instancia de GammaAPI con los datos de la empresa actual (company)
        self.url_base = company.gi_url_base
        self.user = company.gi_user
        self.password = company.gi_password
        self.token = company.gi_token
        self.token_expiration = company.gi_due_data_token
        # Guarda una referencia a la empresa (self.company) para poder actualizarla si se obtiene un nuevo token
        self.company = company

    # Obtiene el token de autenticación de la API de Gamma
    def _get_token(self):

        # Añado cabeceras
        headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, identity",
                "Connection": "keep-alive",
            }

        # Envía una solicitud POST a /login con el usuario y contraseña
        auth_url = f"{self.url_base}/login?"
        response = requests.post(auth_url, data={
            "user": self.user, 
            "password": self.password
        }, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                _logger.error("La respuesta no es JSON válido: %s", response.text)
                raise UserError("La respuesta del servidor no es válida. Verifica el formato del contenido.")

            token = data.get("token")
            expires_at_str = data.get("caducity")

            # Procesar la fecha de expiración
            try:
                expiration = parsedate_to_datetime(expires_at_str)
                if expiration.tzinfo is None:
                    # Si la fecha no tiene información de zona horaria, asumir UTC
                    expiration = expiration.replace(tzinfo=pytz.UTC)
                else:
                    # Convertir a UTC si tiene otra zona horaria
                    expiration = expiration.astimezone(pytz.UTC)
            except Exception as e:
                _logger.warning("Error al procesar la fecha de expiración: %s. Error: %s", expires_at_str, str(e))
                expiration = datetime.now(pytz.UTC) + timedelta(days=1)

            # Convertir a naive datetime antes de guardar en la base de datos
            expiration_naive = expiration.replace(tzinfo=None)

            # Comparar con los valores actuales
            if not self.token or not self.token_expiration:
                # Si no tenemos token ni caducidad guardados, guardamos los nuevos valores
                _logger.info("No hay token o caducidad guardados. Guardando nuevos valores.")
                self.company.sudo().write({
                    'gi_token': token,
                    'gi_due_data_token': expiration_naive
                })
                # Recarga los valores en la instancia
                self.company = self.company.sudo().browse(self.company.id)
                self.token = self.company.gi_token
                self.token_expiration = self.company.gi_due_data_token
                _logger.info("Valores guardados en la compañía: gi_token=%s, gi_due_data_token=%s", token, expiration_naive)
            elif self.token_expiration < datetime.now(pytz.UTC).replace(tzinfo=None):
                # Si el token actual ha expirado, actualizamos con los nuevos valores
                _logger.info("El token actual ha expirado. Actualizando con nuevos valores.")
                self.company.sudo().write({
                    'gi_token': token,
                    'gi_due_data_token': expiration_naive
                })
                # Recarga los valores en la instancia
                self.company = self.company.sudo().browse(self.company.id)
                self.token = self.company.gi_token
                self.token_expiration = self.company.gi_due_data_token
                _logger.info("Valores guardados en la compañía: gi_token=%s, gi_due_data_token=%s", token, expiration_naive)
            else:
                # Si el token actual sigue siendo válido, no hacemos nada
                _logger.info("El token actual sigue siendo válido. No se requiere actualización.")

            # Actualizar los valores en la instancia
            self.token = token
            self.token_expiration = expiration
        else:
            _logger.error("Error al obtener token: %s", response.text)
            raise UserError(f"Error al obtener token: {response.status_code} - {response.text}")

    # Verifica si el token es válido (existe y no ha expirado) y lo renueva si es necesario
    def _ensure_token(self):
        # Convertir datetime.now() a la zona horaria de Madrid
        madrid_tz = pytz.timezone('Europe/Madrid')
        now_in_madrid = datetime.now(pytz.UTC).astimezone(madrid_tz).replace(tzinfo=None)

        # if not self.token or not self.token_expiration or self.token_expiration < datetime.now():
        #     self._get_token()
        if not self.token or not self.token_expiration or self.token_expiration < now_in_madrid:
            self._get_token()        

    # Obtiene la lista de artículos de Gamma
    def get_stock(self):
        # Asegura que el token es válido antes de hacer la solicitud
        self._ensure_token()
        # Realiza una solicitud GET a la API de Gamma para obtener el stock
        url = f"{self.url_base}/stocks?token={self.token}"
        response = requests.get(url)
        # Si la respuesta es exitosa (código 200), devuelve el contenido de la clave "data" del JSON
        # Si no, lanza un error con un mensaje específico
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            raise UserError("Error al obtener stock desde Gamma")

    # Obtiene el stock de un artículo específico por su código
    def get_stock_by_item(self, item_code):
        # Asegura que el token es válido antes de hacer la solicitud
        self._ensure_token()
        # Realiza una solicitud GET a la API de Gamma para obtener el stock del artículo específico
        # La URL incluye el código del artículo y el token de autenticación
        url = f"{self.url_base}/stock/{item_code}?token={self.token}"
        response = requests.get(url)
        # Si la respuesta es exitosa (código 200), devuelve el contenido de la clave "data" del JSON
        # Si no, lanza un error con un mensaje específico
        if response.status_code == 200:
            return response.json().get("data", {}).get(item_code, {})
        else:
            raise UserError(f"Error al obtener stock del artículo {item_code}")
        

    # Obtiene la lista de precios por proveedor desde la API de Gamma
    def get_prices(self):
        """Obtiene la lista de precios desde la API Gamma."""
        self._ensure_token()  # Validar token
        url = f"{self.url_base}/tarifas?token={self.token}"
        try:
            response = requests.get(url, timeout=360)
            if response.status_code == 200:
                return response.json().get("data", [])
            else:
                _logger.error("Error al obtener precios: %s", response.text)
                raise UserError(f"Error al obtener precios: {response.status_code}")
        except Exception as e:
            _logger.exception("Excepción al llamar a la API de precios")
            raise UserError(f"Error en la conexión con Gamma: {str(e)}")
