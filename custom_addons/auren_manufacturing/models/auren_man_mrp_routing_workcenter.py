from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

# XML file generation
from lxml import etree
from xml.etree import ElementTree as ET
from odoo.modules.module import get_module_resource

# create attachment and download
import base64


class ModeloInheritMrpRoutingWorkcenter(models.Model):
    _inherit = "mrp.routing.workcenter"

    template_op = fields.Many2one(
        'auren.man.template.mrp.routing.workcenter', 'Plantilla de operación')

    x_numop = fields.Float(string="Número operación")
    x_minop = fields.Float(string="Minutos operación")

    description = fields.Text(string="Descripción")

    time_start = fields.Float('Setup Time')
    time_stop = fields.Float('Cleanup Time')

    # op_control = fields.Boolean(string='Control',
    #                             default=False)

    @api.onchange("x_numop", "x_minop")
    def _onchange_calculate_timecyclemanual_(self):
        self.time_cycle_manual = self.x_numop * self.x_minop

    # Al cambiar la template de operación se cambia todos los valores de la operación que se esta editando
    @api.onchange("template_op")
    def _onchange_template_op(self):
        for record in self:
            record.name = record.template_op.name
            record.workcenter_id = record.template_op.workcenter_id
            record.company_id = record.template_op.company_id
            record.worksheet_type = record.template_op.worksheet_type
            record.note = record.template_op.note
            record.worksheet = record.template_op.worksheet
            record.worksheet_google_slide = record.template_op.worksheet_google_slide
            record.time_mode_batch = record.template_op.time_mode_batch
            record.time_cycle_manual = record.template_op.time_cycle_manual
            record.time_cycle = record.template_op.time_cycle
            record.x_numop = record.template_op.x_numop
            record.x_minop = record.template_op.x_minop

            record.description = record.template_op.description
            record.time_start = record.template_op.time_start
            record.time_stop = record.template_op.time_stop
            # record.op_control = record.template_op.op_control
