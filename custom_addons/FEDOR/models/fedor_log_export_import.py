from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError


from datetime import timedelta, datetime
import csv


import base64


class FedorExportImportLog(models.Model):
    _name = 'fedor.export.import.log'
    _description = 'Fedor export import log'
    name = fields.Char(index=True, required=True, string="Nombre")
    date_time = fields.Datetime()
    active = fields.Boolean(default=True)
    type = fields.Selection(required=True, selection=[
        ('import', 'Importación'),
        ('export', 'Exportación'),
    ])

    fedor_export_import_log_ids = fields.One2many(
        'fedor.export.import.log.line', 'fedor_export_import_log_id', string='Log',
    )

    order_ids = fields.Many2many('sale.order', string='Pedido')

    def download_file(self):
        attachment_ids = []
        for line in self.fedor_export_import_log_ids:
            attachment_ids.append(line.attachment_id.id)
        # url = '/web/content/download_document?tab_id=%s' % tab_id
        url = '/web/binary/download_document?tab_id=%s' % attachment_ids
        self.sudo().active = False
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def add_line(self, name):
        line = self.env['fedor.export.import.log.line'].create({
            "name": name,
        })
        self.write(
            {'fedor_export_import_log_ids': [(4, line.id, 0)]})

    def add_line_order(self, order_id):
        self.write(
            {'order_ids': [(4, order_id, 0)]})

    def add_line_text_order(self, name, text, encode, file_name):
        adjunto = self.env['ir.attachment'].create({
            'name': file_name,
            'datas': encode,
            'res_model': 'fedor.export.import.log',
            'type': 'binary'
        })

        line = self.env['fedor.export.import.log.line'].create({
            "name": name,
            "attachment_id": adjunto.id,
        })

        self.write(
            {'fedor_export_import_log_ids': [(4, line.id, 0)]})

    def add_line_text(self, name, text, path_txt, file_name):

        adjunto = self.env['ir.attachment'].create({
            'name': file_name,
            'datas': base64.b64encode(open(path_txt, 'rb').read()),
            'res_model': 'fedor.export.import.log',
            'type': 'binary'
        })

        line = self.env['fedor.export.import.log.line'].create({
            "name": name,
            "attachment_id": adjunto.id,
        })

        self.write(
            {'fedor_export_import_log_ids': [(4, line.id, 0)]})
