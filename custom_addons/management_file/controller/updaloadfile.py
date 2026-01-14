from odoo import http
import base64
import chardet
import json

from odoo.http import request

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime


class ControllerUploadFile(http.Controller):
    @http.route('/upload_file', auth='public', methods=['POST'], type='json', csrf=False)
    def upload_file(self):
        try:
            import logging
            _logger = logging.getLogger(__name__)

            # Obtener los datos JSON directamente desde la solicitud HTTP
            data = json.loads(http.request.httprequest.data)
            # Agregar mensaje de depuración
            _logger.info("1")

            file_content_head = data.get('head')
            file_content_line = data.get('line')
            model_name = data.get('model_name')
            name_proces = data.get('name_proces')
            type = data.get('type')
            doc = data.get('doc')
            program = data.get('program')
            user = data.get('user')
            _logger.info("2")
            active_proces = data.get('active_proces')
            _logger.info("3")

            if file_content_head and file_content_line:
                # Decodificar el archivo binario
                file_data_head = base64.b64decode(file_content_head)
                file_data_line = base64.b64decode(file_content_line)
                # Guardar el archivo en el servidor o realizar otras acciones necesarias
                log = request.env[model_name].sudo().create({
                    "name": name_proces,
                    "date_time": datetime.now(),
                    "type": type,
                    "doc": doc,
                    "program": program,
                    "user": user,
                })
                log.add_line_text_order("Importación cabecera correcta",
                                        "", file_content_head, "", "head")
                log.add_line_text_order("Importación líneas correcta",
                                        "", file_content_line, "", "line")
                if (active_proces == "1"):
                    log.process()
                return {'status': 'success', 'message': 'File uploaded successfully'}

            return {'status': 'error', 'message': 'File or file name missing'}
        except Exception as e:
            return {'status': 'error', 'message': f"Ocurrió un error: {e}"}
