from odoo import models, fields, api

class ResCompanyConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gi_url_base = fields.Char(
        string="URL Base",
        readonly=False,
        related='company_id.gi_url_base',
        )
    gi_user = fields.Char(
        string="Usuario Webservice",
        readonly=False,
        related='company_id.gi_user',
        )
    gi_password = fields.Char(
        string="Contraseña Webservice", 
        widget='password',
        readonly=False,
        related='company_id.gi_password',
        )
    gi_token = fields.Char(
        string="Token",
        readonly=False,
        related='company_id.gi_token',
        store=True,
        )
    gi_code_asociate = fields.Char(
        string="Código de Asociado",
        readonly=False,
        related='company_id.gi_code_asociate',
        )
    gi_due_data_token = fields.Datetime(
        string="Fecha de Caducidad del Token",
        readonly=False,
        related='company_id.gi_due_data_token',
        store=True,
        )
    gi_supplier = fields.Many2one(
        'res.partner',
        string="Proveedor Gamma",
        readonly=False,
        related='company_id.gi_supplier',
        )
    gi_viewstocksale = fields.Boolean(
        string="Ver stock en ventas",
        readonly=False,
        related='company_id.gi_viewstocksale',
        )
    gi_tag_gamma = fields.Many2one(
        'product.tag',
        string="Tag Gamma",
        domain="[('id', '!=', False)]",
        readonly=False,
        related='company_id.gi_tag_gamma',
        )
    
    gi_due_data_token_raw = fields.Char(
        string="Fecha de Caducidad del Token",
        readonly=False,
        related='company_id.gi_due_data_token_raw',
    )
