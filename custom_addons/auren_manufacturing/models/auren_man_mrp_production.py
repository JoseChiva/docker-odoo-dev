from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class AurenManMrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            name_var1 = parameters.get_param(
                'auren_otools.var1_s')
            name_var2 = parameters.get_param(
                'auren_otools.var2_s')
            name_var3 = parameters.get_param(
                'auren_otools.var3_s')
            if (name_var1 != False):
                for node in arch.xpath(
                    "//field[@name='var1']"
                ):
                    node.attrib['string'] = name_var1
            if (name_var2 != False):
                for node in arch.xpath(
                    "//field[@name='var2']"
                ):
                    node.attrib['string'] = name_var2
            if (name_var3 != False):
                for node in arch.xpath(
                    "//field[@name='var3']"
                ):
                    node.attrib['string'] = name_var3

            var_readonly = parameters.get_param(
                'auren_otools.var_readonly_s')
            if (var_readonly):
                for node in arch.xpath(
                    "//field[@name='var1']"
                ):
                    node.attrib['readonly'] = '1'
                for node in arch.xpath(
                    "//field[@name='var2']"
                ):
                    node.attrib['readonly'] = '1'
                for node in arch.xpath(
                    "//field[@name='var3']"
                ):
                    node.attrib['readonly'] = '1'

        return arch, view

    # Recalculo para añadir el tiempo de start y stop a nivel de operación

    # def _compute_move_finished_ids(self):
    #     super()._compute_move_finished_ids()
    #     for production in self:
    #         if production.state == 'draft':
    #             workorder_ids = production.workorder_ids
    #             for op in workorder_ids:
    #                 description = op.operation_id.description
    #                 time_start = op.operation_id.time_start
    #                 time_stop = op.operation_id.time_stop
    #                 # op.duration_expected = op.duration_expected+time_start+time_stop
    #                 total_time = ((op.x_numop * op.x_minop *
    #                               op.qty_remaining)+op.time_start+op.time_stop)
    #                 op.duration_expected = total_time
    #     return self

    # Acción del boton de repartimiento de tiempo
    def action_repartimiento_tiempos(self):
        for record in self:
            return {
                'name': _('Repartimiento de tiempo'),
                'string': 'Repartimiento de tiempo',
                'res_model': 'auren.man.repartimiento.tiempo',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': 'frm_auren_man_repartimiento_tiempo',
                'views': [[False, 'form']],
                'context': {
                    'mrp_production_id': record.sudo().id,
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }
