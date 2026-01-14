from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbReportingFormat(models.Model):
    _name = "aurb.rep.format"
    _description = "AURB Reporting Format"

    user_id = fields.Many2one("res.users")
    partner_id = fields.Many2one("res.partner")
    report_id = fields.Many2one("ir.actions.report")
    model_id = fields.Many2one("ir.model")

    @api.onchange('report_id')
    def _onchange_report_id(self):
        for format in self:
            model = self.sudo().env['ir.model'].search([
                ('model', '=', format.report_id.model)
            ])
            format.model_id = model.id

    # type = fields.Char()
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)
