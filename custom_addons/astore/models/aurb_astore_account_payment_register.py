from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _


class AurbaStoreAccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    account_payment_method_payment_bill_ids = fields.One2many(
        "aurb.astore.account.payment.method.payment", "account_payment_method_bill_id")
    account_payment_method_payment_coin_ids = fields.One2many(
        "aurb.astore.account.payment.method.payment", "account_payment_method_coin_id")

    pos_method_payment_id = fields.Many2one(
        "aurb.astore.pos.payment.method",  domain="[('pos_id.id','=',pos_id)]")

    change_cash = fields.Float()
    cash_amount = fields.Float(string="Importe efectivo")

    pos_id = fields.Many2one("aurb.astore.pos")

    type = fields.Selection([
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'Miscellaneous'),
    ])

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        defaults.setdefault('pos_id', user.pos_id.id)
        defaults.setdefault('pos_method_payment_id',
                            user.pos_id.method_payment_id_default.id)

        return defaults

    @api.model
    def create(self, vals):
        parameters = self.env['ir.config_parameter'].sudo()
        max_amount_cash = float(parameters.get_param(
            'astore.max_amount_cash'))

        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        if user.pos_id.id != False:
            if 'type' in vals and 'amount' in vals:
                if (vals['type'] == 'cash'):
                    if (max_amount_cash < vals['amount']):
                        raise ValidationError(
                            "El importe en efectivo no puede ser superior a :"+str(max_amount_cash))
            if not 'pos_method_payment_id' in vals:
                raise ValidationError(
                    "Se debe seleccionar un método de pago")
        records = super().create(vals)
        for record in records:
            if user.pos_id.id != False:
                record.pos_id = user.pos_id.id
        return records

    @api.onchange('pos_method_payment_id')
    def _change_pos_method_payment_id(self):
        self.type = self.pos_method_payment_id.payment_method_id.journal_id.type

        if (self.pos_method_payment_id.payment_method_id.id != False):

            list = get_list_currency(
                self.pos_method_payment_id.payment_method_id.method_payment_currency_ids, self)

            self.account_payment_method_payment_bill_ids = [(5, 0, 0)]
            self.account_payment_method_payment_bill_ids = list[0]

            self.account_payment_method_payment_coin_ids = [(5, 0, 0)]
            self.account_payment_method_payment_coin_ids = list[1]
        self.journal_id = self.pos_method_payment_id.payment_method_id.journal_id.id
        # self.payment_difference = self.amount

    @api.onchange('cash_amount')
    def change_cash_amount(self):
        for record in self:
            total = record.cash_amount
            record.amount = total
            if (record.payment_difference < 0):
                diff = record.payment_difference
                record.amount = record.amount+diff
                record.change_cash = -diff

    @api.onchange('account_payment_method_payment_bill_ids', 'account_payment_method_payment_coin_ids')
    def _calculation_cash(self):
        for record in self:
            total = 0
            if (record.type == "cash"):
                for val in record.account_payment_method_payment_bill_ids:
                    val_number = val.number
                    val_currency = val.method_payment_currency_id.value
                    total = total+(val_number*val_currency)
                    record.cash_amount = total
                for val in record.account_payment_method_payment_coin_ids:
                    val_number = val.number
                    val_currency = val.method_payment_currency_id.value
                    total = total+(val_number*val_currency)

                record.amount = total
                if (record.payment_difference < 0):
                    diff = record.payment_difference
                    record.amount = record.amount+diff
                    record.change_cash = -diff


def get_list_currency(currencies, self):
    lines_bill = []
    lines_coin = []

    for cur in currencies:

        if (cur.type == "coin"):
            vals = (
                {"account_payment_method_coin_id": self,
                 "method_payment_currency_id": cur.id,
                 "order": cur.order,
                 }
            )
            lines_coin.append(vals)
        else:
            vals = (
                {"account_payment_method_bill_id": self,
                 "method_payment_currency_id": cur.id,
                 "order": cur.order, }
            )
            lines_bill.append(vals)

    lines_bill.sort(key=lambda x: x['order'], reverse=False)
    lines_coin.sort(key=lambda x: x['order'], reverse=False)

    lines_bill_2 = []
    lines_coin_2 = []

    for val in lines_bill:
        valor = (0, 0, val)
        lines_bill_2.append(valor)
    for val in lines_coin:
        valor = (0, 0, val)
        lines_coin_2.append(valor)
    return [lines_bill_2, lines_coin_2]
