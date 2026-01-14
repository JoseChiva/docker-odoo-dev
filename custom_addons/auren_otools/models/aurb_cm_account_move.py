from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbCmAccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        parameters = self.env['ir.config_parameter'].sudo()
        journal_for_location = parameters.get_param(
            'auren_otools.journal_for_location')
        invoices = super().create(vals)
        if (journal_for_location):
            cid = self.env.company.id
            # for val in vals:

            for invoice in invoices:
                # Saltamos de las líneas de la factura a las líneas del pedido
                # Cuando tenemos las líneas del pedidos saltamos a las líneas de la entrega y obtenemos el almacén
                # Cuando tenemos el almacen obtenemos el id del journal para ese almacen
                journal_id = invoice.line_ids.sale_line_ids.move_ids.picking_id.location_id.journal_id.id

                # sale_id = self.env['account.journal'].search(
                #     domain=[('name', '=', journal_id),
                #             ('type', '=', 'sale'),
                #             ('company_id', '=', cid)],
                #     limit=1,
                # )
                if journal_id != False:
                    invoice.journal_id = journal_id
        return invoices
