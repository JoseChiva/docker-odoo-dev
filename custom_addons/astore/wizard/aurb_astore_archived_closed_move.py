from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import date


class AurbaStoreArchivedClosedMove(models.TransientModel):
    _name = "aurb.astore.archived.close.move"
    name = fields.Char()
    pos_id = fields.Many2one(
        "aurb.astore.pos",  required=True, index=True)
    from_date = fields.Date()
    to_date = fields.Date(required=True)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        defaults.setdefault('pos_id', user.pos_id.id)
        defaults.setdefault('to_date', date.today())

        return defaults

    def action_archived(self):
        for record in self:
            from_date = record.from_date
            to_date = record.to_date

            if from_date:
                move_closed = self.sudo().env['aurb.astore.close.pos'].search([
                    ('posted', '=', True),
                    ('pos_id', '=', record.pos_id.id),
                    ('date', '>=', from_date),
                    ('date', '<=', to_date)
                ])
            else:
                move_closed = self.sudo().env['aurb.astore.close.pos'].search([
                    ('posted', '=', True),
                    ('pos_id', '=', record.pos_id.id),
                    ('date', '<=', to_date)
                ])

            for record_close in move_closed:
                for record_move in record_close.move_ids:
                    record_move.active = False
                record_close.active = False

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.pos_id.name+' ' + \
                str(record.from_date)+' '+str(record.to_date)
            record.display_name = view_name
