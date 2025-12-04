from odoo import models, fields, api, tools, Command
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbastorePos(models.Model):
    _name = "aurb.astore.pos"
    _description = "AURB aStore TPV"

    _sql_constraints = [
        ('pk_astore_pos', 'unique(code, name)',
         'Ya existe un TPV con este código/nombre'),
    ]

    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    code = fields.Char(index=True, required=True, size=5)
    separator = fields.Char(index=True, size=1)
    name = fields.Char(index=True, required=True)
    active = fields.Boolean(default=True)

    method_payment_id = fields.Many2one(
        "aurb.astore.pos.payment.method",

        domain="[('pos_id.id','=',id)]"
    )
    method_payment_id_default = fields.Many2one(
        "aurb.astore.pos.payment.method",

        domain="[('pos_id.id','=',id)]"
    )

    # sale_order_prefix = fields.Char("Prefijo pedido de ventas")
    # delivery_prefix = fields.Char("Prefijo albaran de ventas")
    stock_location_id = fields.Many2one(
        "stock.location",
        required=True
    )

    move_ids = fields.One2many(
        "aurb.astore.move.pos", "pos_id", string="move_ids_pos")

    user_ids = fields.One2many("res.users", "pos_id")

    payment_method_ids = fields.One2many(
        "aurb.astore.pos.payment.method", "pos_id")

    account_id = fields.Many2one(
        "account.account", string="account_pos",  requerid=True)

    account_profit_loss_id = fields.Many2one(
        "account.account",  requerid=True)

    account_income_id = fields.Many2one(
        "account.account",  requerid=True)

    order_count = fields.Integer(compute='get_order_count')
    delivery_count = fields.Integer(compute='get_delivery_count')
    invoice_count = fields.Integer(compute='get_invoice_count')

    close_count = fields.Integer(compute='get_close_count')

    journal_close_id = fields.Many2one(
        "account.journal",
        required=True
    )

    def get_order_count(self):
        count = self.env['sale.order'].search_count(
            [('pos_id', '=', self.id)])
        self.order_count = count

    def get_delivery_count(self):
        count = self.env['stock.picking'].search_count(
            [('pos_id', '=', self.id)])
        self.delivery_count = count

    def get_invoice_count(self):
        count = self.env['account.move'].search_count(
            [('pos_id', '=', self.id), ('move_type', '=', 'out_invoice')])
        self.invoice_count = count

    def get_close_count(self):
        count = self.env['aurb.astore.close.pos'].search_count(
            [('pos_id', '=', self.id)])
        self.close_count = count
