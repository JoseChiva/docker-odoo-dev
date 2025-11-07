from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


def get_format_print(partner_id, self):
    name_model = self._name
    model = self.sudo().env['ir.model'].search([
        ('model', '=', name_model)
    ])

    company_id = self.env.company.id
    current_uid = self._uid
    report = self.sudo().env['aurb.rep.format'].search([
        ('model_id', '=', model.id),
        ('company_id', '=', company_id),
        '|',
        ('user_id', '=', current_uid),
        ('user_id', '=', False),
        '|',
        ('partner_id', '=', partner_id),
        ('partner_id', '=', False)
    ], order='user_id,partner_id asc')
    for rep in report:
        return rep.report_id
    return False
