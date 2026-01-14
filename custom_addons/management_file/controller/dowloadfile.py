from odoo import http
import base64
import chardet
import json

from odoo.http import request

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime


class ControllerDownloadFile(http.Controller):
    @http.route('/download_file', auth='public', methods=['POST'], type='json', csrf=False)
    def download_file(self):
        import logging
        _logger = logging.getLogger(__name__)

        # Obtener los datos JSON directamente desde la solicitud HTTP
        data = json.loads(http.request.httprequest.data)
        # Agregar mensaje de depuración
        _logger.info("Received data: %s", data)

        model_name = data.get('model_name')
        name_proces = data.get('name_proces')
        type = data.get('type')
        doc = data.get('doc')
        program = data.get('program')
        user = data.get('user')
        files_data = []
        registros = request.env[model_name].sudo().search(
            [('type', '=', type), ('program', '=', program), ('doc', '=', doc), ('exported', '=', False), ('user', '=', user)])
        for registro in registros:
            for attach in registro.get_lines():
                if (attach.attachment_id):
                    data = attach.attachment_id.datas
                    file_data = {
                        'type': attach.type,
                        'file_data': data,  # Ya está en base64
                    }
                    files_data.append(file_data)
        if (files_data):
            for registro in registros:
                registro.exported = True
            return {'status': 'success', 'message': files_data}

        return {'status': 'error', 'message': 'File or file name missing'}
