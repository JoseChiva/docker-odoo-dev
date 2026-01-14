# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Auren_Cst_ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_cost_standard = fields.Boolean(
        default=False, string="Cost standard", implied_group='cost_standard_extended.group_cost_standard')
