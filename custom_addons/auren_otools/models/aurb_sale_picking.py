from odoo import Command, api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class AurenSalesPicking(models.Model):
    _name = 'aurb.sale.picking'
    _description = 'Picking'
    _order = 'id'
    name = fields.Char(index=True)
    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    carrier_id = fields.Many2one(
        'delivery.carrier', required=True)

    date = fields.Date(
        'Fecha', default=fields.Date.today() + relativedelta(days=1), required=True)

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('pend', 'Pendiente'),
        ('prepa', 'Preparando'),
        ('prep', 'Preparado'),
        ('entr', 'Entregado')], 'Estado', default="pend")

    stock_move_ids = fields.Many2many(
        "stock.move", domain="[('state','in',('waiting','confirmed','partially_available','assigned'))]")

    sale_order_line_ids = fields.Many2many(
        "sale.order.line", domain="[('state','in',('draft','sent'))]")

    pending_line = fields.Float(
        string="Líneas pendientes", compute="_compute_cost_product")

    def _number_pending_line(self):
        for pick in self:
            self.pending_line = 0
            for order in self.sale_order_line_ids:
                if (order.pick_delivery == False):
                    self.pending_line += 1

    @api.onchange('carrier_id', 'date')
    def _change_carrier_id_date(self):
        for sale_picking in self:
            if (sale_picking.carrier_id):
                fecha = sale_picking.date.strftime("%m/%d/%Y")
                sale_picking.name = sale_picking.carrier_id.name + \
                    " ("+fecha+") "

    def action_get_not_delivery_lines(self):
        for pick in self:
            search_sale_picking = self.sudo().env['aurb.sale.picking'].search([
                ('state', '=', 'entr'),
                ('pending_line', '>', 0),
                ('carrier_id', '=', pick.carrier_id.id),
                ('id', '!=', pick.id),
                ('date', '<', pick.date),
            ])
            for pick_search in search_sale_picking:
                for order_line in pick_search.sale_order_line_ids:
                    if (order_line.pick_delivery == False):
                        pick.sale_order_line_ids = [(4, order_line.id)]
