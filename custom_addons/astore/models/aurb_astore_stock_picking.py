from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbaStoreStockPicking(models.Model):
    _inherit = "stock.picking"

    pos_id = fields.Many2one("aurb.astore.pos")
    user_pos = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        # defaults.setdefault('user_pos', False)

        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        if user.pos_id.id != False:
            defaults.setdefault('user_pos', True)
            defaults.setdefault('pos_id', user.pos_id.id)

        return defaults

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

        # for record in records:
        #     if (record.picking_type_id.code == 'outgoing'):
        #         if id_pos_user != False:
        #             record.pos_id = id_pos_user
        #             code = user.pos_id.code
        #             separator = user.pos_id.separator
        #             record.name = code+separator+record.name
        #             record.location_id = user.pos_id.stock_location_id.id

        return records
