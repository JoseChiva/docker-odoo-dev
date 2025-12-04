from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbaStoreAccountMove(models.Model):
    _inherit = "account.move"

    user_pos = fields.Boolean()

    pos_id = fields.Many2one("aurb.astore.pos")
    type = fields.Selection(selection=[
        ('in', 'In'),
        ('out', 'Out'),
        ('cls', 'Close'),
    ])

    @api.model
    def create(self, vals):
        records = super().create(vals)
        for invoice in records:
            if (invoice.move_type) == 'out_invoice':
                pos_invoice = invoice.invoice_line_ids.sale_line_ids.order_id.pos_id
                if pos_invoice.id != False:
                    invoice.pos_id = pos_invoice.id

            elif (invoice.move_type) == 'entry':
                current_uid = self._uid
                user = self.sudo().env['res.users'].browse(current_uid)
                if user.pos_id.id != False:
                    pos_user = user.pos_id
                    invoice.pos_id = pos_user.id

        return records

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        if user.pos_id.id != False:
            defaults.setdefault('user_pos', True)
            defaults.setdefault('pos_id', user.pos_id.id)
        return defaults

    @api.model
    def write(self, vals):

        for account_move in self:
            if 'state' in vals and vals['state'] == 'posted' and account_move.state == 'draft':
                # if (account_move.move_type) == 'out_invoice':
                # pos_invoice = invoice.pos_id.id
                # if (pos_invoice != False):
                #     invoice_date = invoice.invoice_date
                #     amount_total = invoice.amount_total
                #     account_move_id = invoice.id
                #     invoice.env["aurb.astore.move.pos"].create({
                #         "pos_id": pos_invoice,
                #         "date": invoice_date,
                #         "amount": amount_total,
                #         "account_move_id": account_move_id,

                #     })

                # No tengo claro que se tenga que quitar la línea if (account_move.move_type) == 'entry':
                # Quitamos esta línea ya que al parecer antes odoo apart del propio movimiento generaba un asiento, pero ahora ya no
                # ahora solo genera el propio movimiento del documento
                if (account_move.move_type) == 'entry':
                    if (account_move.type != "cls"):
                        pos_journal = account_move.pos_id.id
                        type_move = 'general'
                        if (pos_journal != False):
                            if (account_move.journal_id.type != False):
                                type_journal = account_move.journal_id.type
                                type_move = type_journal

                            date = account_move.date
                            amount_total = account_move.amount_total
                            if (account_move.type == "out"):
                                amount_total = -amount_total
                            account_move_id = account_move.id
                            account_move.sudo().env["aurb.astore.move.pos"].create({
                                "pos_id": pos_journal,
                                "date": date,
                                "amount": amount_total,
                                "account_move_id": account_move_id,
                                "type": type_move,
                            })

        return super(AurbaStoreAccountMove, self).write(vals)

    def action_register_payment(self):
        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        if user.pos_id.id != False:
            # return {
            #     'name': _('Register Payment'),
            #     'res_model': 'account.payment.register',
            #     'view_mode': 'form',
            #     'views': [[False, 'form']],
            #     'context': {
            #         'active_model': 'account.move',
            #         'active_ids': self.ids,
            #     },
            #     'target': 'new',
            #     'type': 'ir.actions.act_window',
            # }
            return {
                'name': _('Auren aStore Payment Register'),
                'res_model': 'account.payment.register',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': 'act_aurb_astore_payment_register',
                'views': [[False, 'form']],
                'context': {
                    'active_model': 'account.move',
                    'active_ids': self.sudo().ids,
                    'invisible_new_field': False,
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }
        return super(AurbaStoreAccountMove, self).action_register_payment()
