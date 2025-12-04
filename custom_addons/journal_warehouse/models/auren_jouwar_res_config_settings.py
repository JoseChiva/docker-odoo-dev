# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AurenJouWarResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    journal_for_location = fields.Boolean(
        default=False, string="Diario contable por almacén", config_parameter='journal_warehouse.journal_for_location')
