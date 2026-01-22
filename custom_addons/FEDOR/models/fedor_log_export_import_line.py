from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

from odoo.modules.module import get_module_resource
import base64

from datetime import timedelta, datetime
import csv


class FedorExportImportLogLine(models.Model):
    _name = 'fedor.export.import.log.line'
    _description = 'Fedor export import log line'

    name = fields.Char(index=True, required=True, string="Descripción")

    fedor_export_import_log_id = fields.Many2one(
        'fedor.export.import.log', 'Log',
    )

    attachment_id = fields.Many2one(
        'ir.attachment', 'File',
    )

    def download_file(self):
        # url = '/web/content/download_document?tab_id=%s' % tab_id
        url = '/web/content/%s?download=true' % self.attachment_id.id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
