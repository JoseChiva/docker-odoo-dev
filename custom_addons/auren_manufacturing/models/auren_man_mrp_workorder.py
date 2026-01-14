from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class AurenManMrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    description = fields.Text(string="Descripción")

    time_start = fields.Float(
        'Setup Time', compute="_compute_time", store=True)
    time_stop = fields.Float(
        'Cleanup Time', compute="_compute_time", store=True)

    x_numop = fields.Float(string="Número operación",
                           compute="_compute_time", store=True)
    x_minop = fields.Float(string="Minutos operación",
                           compute="_compute_time", store=True)

    @api.onchange("x_numop", "x_minop", "time_start", "time_stop", "workcenter_id")
    def _onchange_calculate_timecyclemanual_(self):
        for op in self:
            total_time = ((
                op.x_numop * op.x_minop*op.qty_remaining)+op.time_start+op.time_stop)
            op.duration_expected = total_time

    def _get_duration_expected(self, alternative_workcenter=False, ratio=1):
        total_time = self.time_start+self.time_stop
        return super()._get_duration_expected(alternative_workcenter, ratio)+total_time

    @api.depends('operation_id')
    def _compute_time(self):
        for op in self:
            if (op.operation_id):
                op.description = op.operation_id.description
                op.time_start = op.operation_id.time_start
                op.time_stop = op.operation_id.time_stop
                op.x_numop = op.operation_id.x_numop
                op.x_minop = op.operation_id.x_minop
