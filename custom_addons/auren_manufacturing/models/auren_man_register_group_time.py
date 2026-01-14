from odoo import Command, api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError

from datetime import timedelta, datetime


class AurenManRegisterGroupTime(models.Model):
    _name = 'auren.man.register.group.time'
    _description = 'Registro de tiempo agrupado'
    _order = 'id'
    name = fields.Char(index=True, required=True)
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    active = fields.Boolean(default=True)

    employee_assigned_id = fields.Many2one(
        'hr.employee', 'Empleado',  required=True,
    )
    workorder_ids = fields.Many2many(
        "mrp.workorder",  required=True, domain="[('state','in',('ready','progress','waiting'))]")

    workcenter_prod_ids = fields.Many2many(
        "mrp.workcenter.productivity")

    workcenter_id = fields.Many2one(
        "mrp.workcenter",  required=True)

    loss_id = fields.Many2one(
        'mrp.workcenter.productivity.loss', "Productividad",
        ondelete='restrict', required=True)

    date_start = fields.Datetime(
        'Fecha inicio', default=fields.Datetime.now, required=True)
    date_end = fields.Datetime('Fecha final')
    duration = fields.Float(
        'Duration', compute='_compute_duration', store=True)

    state = fields.Selection([
        ('pend', 'Pendiente'),
        ('start', 'Iniciado'),
        ('reg', 'Registrado'),
        ('end', 'Cerrado')], 'Estado', default="pend")

    @api.model
    def create(self, vals):
        if ('workorder_ids' not in vals or len(vals['workorder_ids']) == 0):
            raise ValidationError(
                "No se han seleccionado operaciones")
        records = super().create(vals)
        return records

    @api.depends('date_end', 'date_start')
    def _compute_duration(self):
        for blocktime in self:
            if blocktime.date_start and blocktime.date_end:
                blocktime.duration = blocktime.loss_id._convert_to_duration(blocktime.date_start.replace(
                    microsecond=0), blocktime.date_end.replace(microsecond=0), blocktime.workcenter_id)
            else:
                blocktime.duration = 0.0

    @api.onchange('duration')
    def _duration_changed(self):
        if self.date_end and self.state != "pend":
            self.date_start = self.date_end - timedelta(minutes=self.duration)
            self._loss_type_change()

    def start_time(self):

        cid = self.env.company.id
        self.date_start = date = datetime.now()
        self.date_end = False
        self .duration = 0
        self.state = "start"

        main_employee = self.employee_assigned_id.id

        for wo in self.workorder_ids:
            # res = super().button_start()
            if len(wo.time_ids) == 1 or all(wo.time_ids.mapped('date_end')):
                for check in wo.check_ids:
                    if check.component_id:
                        check._update_component_quantity()

            if main_employee:
                if len(wo.allowed_employees) == 0 or main_employee in [emp.id for emp in wo.allowed_employees]:
                    wo.ensure_one()
                    time_data = wo._prepare_timeline_vals(
                        wo.duration, fields.Datetime.now())
                    time_data['employee_id'] = self.employee_assigned_id.id
                    time_data['workcenter_id'] = self.workcenter_id.id
                    time_data['loss_id'] = self.loss_id.id
                    move = self.env['mrp.workcenter.productivity'].create(
                        time_data)
                    self.write(
                        {'workcenter_prod_ids': [(4, move.id, 0)]})
                    wo.state = "progress"

                    wo.employee_ids |= self.env['hr.employee'].browse(
                        main_employee)

    # def start_time_2(self):

    #     for op in self.workorder_ids:

    #         move = self.sudo().env["mrp.workcenter.productivity"].create({
    #             "company_id": cid,
    #             "workcenter_id": self.workcenter_id.id,
    #             "employee_id": self.employee_assigned_id.id,
    #             "date_start": self.date_start,
    #             # "date_end": self.date_end,
    #             # "duration": self.duration,
    #             "production_id": op.workcenter_id.id,
    #             "workorder_id": op.id,
    #             "loss_id": self.loss_id.id,
    #         })
    #         self.write({'workcenter_prod_ids': [(4, move.id, 0)]})
    #         # repartition_line.write({'tag_ids': [(4, tax_line_tag.id, 0)]})
    #         # self.workcenter_prod_ids.append([(4, [move.id])])


# underperformance_timers = self.env['mrp.workcenter.productivity']
#         for timer in self:
#             wo = timer.workorder_id
#             timer.write({'date_end': fields.Datetime.now()})
#             if wo.duration > wo.duration_expected:
#                 productive_date_end = timer.date_end - relativedelta.relativedelta(minutes=wo.duration - wo.duration_expected)
#                 if productive_date_end <= timer.date_start:
#                     underperformance_timers |= timer
#                 else:
#                     underperformance_timers |= timer.copy({'date_start': productive_date_end})
#                     timer.write({'date_end': productive_date_end})
#         if underperformance_timers:
#             underperformance_type = self.env['mrp.workcenter.productivity.loss'].search([('loss_type', '=', 'performance')], limit=1)
#             if not underperformance_type:
#                 raise UserError(_("You need to define at least one unactive productivity loss in the category 'Performance'. Create one from the Manufacturing app, menu: Configuration / Productivity Losses."))
#             underperformance_timers.write({'loss_id': underperformance_type.id})


    def end_time(self):
        self.date_end = date = datetime.now()
        self.state = "reg"

        date_start = self.date_start
        total_duration = 0
        for op in self.workorder_ids:
            total_duration = total_duration+op.duration_expected

        for register in self.workcenter_prod_ids:
            if (register.date_end == False):
                duration_expected = register.workorder_id.duration_expected
                time_to_registred = (
                    (duration_expected/total_duration)*self.duration)
                # self.date_end

                time_change = timedelta(minutes=time_to_registred)

                register.date_start = date_start
                register.date_end = date_start+time_change
                register.duration = time_to_registred
                date_start = date_start+time_change

    def close_time(self):
        self.state = "end"
        self.active = False
