from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import _


class AurenManMrpReportBomStructure(models.AbstractModel):
    _inherit = "report.mrp.report_bom_structure"

    # Remplazamos la función estandard de calculo de tiempo para incluir el tiempo de start y stop de las operaciones
    @api.model
    def _get_operation_line(self, product, bom, qty, level, index):
        operations_list = super()._get_operation_line(product, bom, qty, level, index)

        for operation_item in operations_list:
            operation = operation_item['operation']
            time_start = operation.time_start
            time_stop = operation.time_stop
            duration_expected = operation_item['quantity'] + \
                time_start+time_stop
            operation_item['quantity'] = duration_expected
            total = self._get_operation_cost(
                (time_start+time_stop), operation)
            bom_cost = self.env.company.currency_id.round(
                total)
            operation_item['bom_cost'] = operation_item['bom_cost'] + bom_cost
        return operations_list
