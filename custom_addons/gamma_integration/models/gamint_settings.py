from odoo import models, fields
from odoo.exceptions import ValidationError

class ResCompany(models.Model):
    _inherit = 'res.company'

    gi_url_base = fields.Char(
        string="URL Base",
        readonly=False,
        )
    gi_user = fields.Char(
        string="Usuario Webservice",
        readonly=False,
        )
    gi_password = fields.Char(
        string="Contraseña Webservice",
        widget='password',
        readonly=False,
        )
    gi_token = fields.Char(
        string="Token",
        readonly=False,
        store=True,
        )
    gi_code_asociate = fields.Char(
        string="Código de Asociado",
        readonly=False,
        )
    gi_due_data_token = fields.Datetime(
        string="Fecha de Caducidad del Token",
        readonly=False,
        store=True,
        )
    gi_supplier = fields.Many2one(
        'res.partner',
        string="Proveedor Gamma",
        readonly=False,
        )
    gi_viewstocksale = fields.Boolean(
        string="Ver stock en ventas",
        readonly=False,
        )
    gi_tag_gamma = fields.Many2one(
        'product.tag',
        string="Tag Gamma",
        domain="[('id', '!=', False)]",
        readonly=False,
        )
    
    gi_due_data_token_raw = fields.Char(
        compute="_compute_gi_due_data_token_raw",
        string="Token Expira (UTC crudo)"
    )

    def _compute_gi_due_data_token_raw(self):
        for rec in self:
            rec.gi_due_data_token_raw = rec.gi_due_data_token and rec.gi_due_data_token.strftime("%Y-%m-%d %H:%M:%S") or ""
