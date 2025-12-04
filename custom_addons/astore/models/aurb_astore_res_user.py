from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbaStoreResUsers(models.Model):
    _inherit = "res.users"

    pos_id = fields.Many2one(
        "aurb.astore.pos",
    )

    rol_astore = fields.Char(compute="_rolgroup")

    @api.depends("pos_id")
    def _rolgroup(self):
        for user in self:
            if (user.has_group('astore.astore_admin_group')):
                user.rol_astore = _('Admin')
            elif (user.has_group('astore.astore_pos_group')):
                user.rol_astore = _('Admin POS')
            elif (user.has_group('astore.astore_user_group')):
                user.rol_astore = _('User')
            else:
                user.rol_astore = _('Sin rol')
