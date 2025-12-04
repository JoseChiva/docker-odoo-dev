from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbaStoreStockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):

        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        id_pos_user = user.pos_id.id
        if id_pos_user == False:
            context = self._context
            current_uid = context.get('uid')
            user = self.sudo().env['res.users'].browse(current_uid)
            id_pos_user = user.pos_id.id

        records = super().create(vals)

        for record in records:
            if (record.sale_line_id):
                if id_pos_user != False:
                    if (record.group_id):
                        if (len(record.group_id.stock_move_ids) == 1):
                            record.location_id = user.pos_id.stock_location_id.id

        return records
