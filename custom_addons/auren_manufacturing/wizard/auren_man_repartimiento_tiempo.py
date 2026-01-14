from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

from datetime import date, timedelta, datetime


class AurenManRepartimientoTiempo(models.TransientModel):
    _name = "auren.man.repartimiento.tiempo"

    mrp_production_id = fields.Many2one(
        "mrp.production",  required=True)
    employee_assigned_id = fields.Many2one(
        'hr.employee',  required=True
    )
    loss_id = fields.Many2one(
        'mrp.workcenter.productivity.loss', "Loss Reason", required=True)

    time_total = fields.Float(
        'Tiempo total',  required=True)

    # Cargamos los valores por defecto
    # Orden de producción

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        context = dict(self.env.context or {})
        mrp_production_id = context.get('mrp_production_id')
        defaults.setdefault('mrp_production_id', mrp_production_id)
        return defaults

    # Al ejecutar el boton de reparto, esta función repartira equitativamente los tiempos
    # segun los tiempo que hay en la expectativa, tambien descuenta los tiempos ya introducidos,
    # para que el total cuadre con el tiempo a repartir
    # Cuando lo tiene calculado crea un movimiento de tiempo con el operario seleccionado
    def action_repartimiento_tiempos(self):
        for record in self:
            cid = record.env.company.id

            mrp_production_id = record.mrp_production_id.id
            employee_assigned_id = record.employee_assigned_id.id
            loss_id = record.loss_id.id

            time_total = record.time_total
            operations = self.sudo().env['mrp.workorder'].search([
                ('production_id', '=', mrp_production_id),
            ])
            browse_operations = self.sudo().env["mrp.workorder"].browse(
                operations)
            total_duration = 0
            for op in operations:
                total_duration = total_duration+op.duration_expected

            for op in operations:
                duration_expected = op.duration_expected
                workcenter_productivity = self.sudo().env['mrp.workcenter.productivity'].search([
                    ('production_id', '=', mrp_production_id),
                    ('workorder_id', '=', op.id),
                ])

                browse_workcenter_productivity = self.sudo().env["mrp.workcenter.productivity"].browse(
                    workcenter_productivity)
                total_time_registred = 0
                for reg_workcenter_productivity in browse_workcenter_productivity:
                    total_time_registred = total_time_registred + \
                        reg_workcenter_productivity.id.duration

                time_to_registred = round((
                    (duration_expected/total_duration)*time_total)-total_time_registred, 2)

                time_change = timedelta(minutes=time_to_registred)

                date = datetime.now()
                date_start = date-time_change
                date_end = date

                duration = record.loss_id._convert_to_duration(date_start.replace(
                    microsecond=0), date_end.replace(microsecond=0),  op.workcenter_id)

                time_data = op._prepare_timeline_vals(
                    op.duration, date_start)
                time_data['employee_id'] = employee_assigned_id
                time_data['workcenter_id'] = op.workcenter_id.id
                time_data['loss_id'] = loss_id
                time_data['date_end'] = date_end
                time_data['duration'] = time_to_registred
                move = self.env['mrp.workcenter.productivity'].create(
                    time_data)

                # move = record.sudo().env["mrp.workcenter.productivity"].create({
                #     "company_id": cid,
                #     "workcenter_id": op.workcenter_id.id,
                #     "employee_id": employee_assigned_id,
                #     "date_start": date_start,
                #     "date_end": date_end,
                #     "duration": time_to_registred,
                #     "production_id": mrp_production_id,
                #     "workorder_id": op.id,
                #     "loss_id": loss_id,
                # })
