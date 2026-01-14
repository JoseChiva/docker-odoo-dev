
from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

# Clase para la gestión de las template de lal operación
# En la mayoria de campos es una copia del objeto mrp.routing.workcenter


class AurenManTemplateMrpRoutingWorkcenter(models.Model):
    _name = 'auren.man.template.mrp.routing.workcenter'
    _description = 'Work Center Usage'
    _order = 'id'
    _check_company_auto = True

    name = fields.Char('Operation', required=True)
    active = fields.Boolean(default=True)
    workcenter_id = fields.Many2one(
        'mrp.workcenter', 'Work Center', required=True, check_company=True)

    company_id = fields.Many2one(
        'res.company', 'Company', default=lambda self: self.env.company)
    worksheet_type = fields.Selection([
        ('pdf', 'PDF'), ('google_slide', 'Google Slide'), ('text', 'Text')],
        string="Worksheet", default="text"
    )
    note = fields.Html('Description')
    worksheet = fields.Binary('PDF')
    worksheet_google_slide = fields.Char(
        'Google Slide', help="Paste the url of your Google Slide. Make sure the access to the document is public.")
    time_mode = fields.Selection([
        ('auto', 'Compute based on tracked time'),
        ('manual', 'Set duration manually')], string='Duration Computation',
        default='manual')
    time_mode_batch = fields.Integer('Based on', default=10)
    time_computed_on = fields.Char(
        'Computed on last', compute='_compute_time_computed_on')
    time_cycle_manual = fields.Float(
        'Manual Duration', default=60,
        help="Time in minutes:"
        "- In manual mode, time used"
        "- In automatic mode, supposed first time when there aren't any work orders yet")
    time_cycle = fields.Float('Duration', compute="_compute_time_cycle")

    description = fields.Text(string="Descripción")

    time_start = fields.Float('Setup Time')
    time_stop = fields.Float('Cleanup Time')

    # op_control = fields.Boolean(string='Control',
    #                             default=False)

    @api.depends('time_mode', 'time_mode_batch')
    def _compute_time_computed_on(self):
        for operation in self:
            operation.time_computed_on = _(
                '%i work orders', operation.time_mode_batch) if operation.time_mode != 'manual' else False

    @api.depends('time_cycle_manual', 'time_mode')
    def _compute_time_cycle(self):
        manual_ops = self.filtered(
            lambda operation: operation.time_mode == 'manual')
        for operation in manual_ops:
            operation.time_cycle = operation.time_cycle_manual
        for operation in self - manual_ops:
            data = self.env['mrp.workorder'].search([
                ('operation_id', '=', operation.id),
                ('qty_produced', '>', 0),
                ('state', '=', 'done')],
                limit=operation.time_mode_batch,
                order="date_finished desc, id desc")
            # To compute the time_cycle, we can take the total duration of previous operations
            # but for the quantity, we will take in consideration the qty_produced like if the capacity was 1.
            # So producing 50 in 00:10 with capacity 2, for the time_cycle, we assume it is 25 in 00:10
            # When recomputing the expected duration, the capacity is used again to divide the qty to produce
            # so that if we need 50 with capacity 2, it will compute the expected of 25 which is 00:10
            total_duration = 0  # Can be 0 since it's not an invalid duration for BoM
            # Never 0 unless infinite item['workcenter_id'].capacity
            cycle_number = 0
            for item in data:
                total_duration += item['duration']
                capacity = item['workcenter_id']._get_capacity(item.product_id)
                cycle_number += tools.float_round(
                    (item['qty_produced'] / capacity or 1.0), precision_digits=0, rounding_method='UP')
            if cycle_number:
                operation.time_cycle = total_duration / cycle_number
            else:
                operation.time_cycle = operation.time_cycle_manual

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        return res

    def write(self, vals):
        res = super().write(vals)
        return res

    def action_archive(self):
        res = super().action_archive()
        bom_lines = self.env['mrp.bom.line'].search(
            [('operation_id', 'in', self.ids)])
        bom_lines.write({'operation_id': False})
        return res

    def action_unarchive(self):
        res = super().action_unarchive()
        return res

    x_numop = fields.Float(string="Número operación")
    x_minop = fields.Float(string="Minutos operación")

    @api.onchange("x_numop", "x_minop")
    def _onchange_calculate_timecyclemanual_(self):
        self.time_cycle_manual = self.x_numop * self.x_minop
