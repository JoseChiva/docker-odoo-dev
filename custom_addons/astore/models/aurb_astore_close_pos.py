from odoo import models, fields, api, tools, Command

from odoo.exceptions import UserError, ValidationError
from odoo import _


from datetime import date


class AurbastoreCloseTpv(models.Model):
    _name = "aurb.astore.close.pos"
    _description = "AURB aStore Cierre TPV"

    # _sql_constraints = [
    #     ('pk_astore_close_pos', 'unique(pos_id, date)',
    #      'No puede haber mas de un cierre por dia / TPV'),
    # ]

    name = fields.Char(index=True)

    company_id = fields.Many2one(
        'res.company', required=True, readonly=True, default=lambda self: self.env.company)

    pos_id = fields.Many2one(
        "aurb.astore.pos",  required=True, index=True)

    active = fields.Boolean(default=True)
    date = fields.Date(required=True, index=True)

    amount = fields.Float(string="amount_close")

    account_payment_method_payment_bill_ids = fields.One2many(
        "aurb.astore.close.pos.method.payment", "account_payment_method_bill_id")
    account_payment_method_payment_coin_ids = fields.One2many(
        "aurb.astore.close.pos.method.payment", "account_payment_method_coin_id")

    amount_cash_total = fields.Float()

    amount_cash = fields.Float()
    amount_general = fields.Float()

    amount_income = fields.Float()
    amount_diff = fields.Float()
    posted = fields.Boolean(default=False)

    move_ids = fields.One2many(
        "aurb.astore.move.pos", "close_pos_id", string="move_ids_close")

    move_id = fields.Many2one("account.move", string="move_id_close")
    move_income_id = fields.Many2one("account.move")

    amount_pos = fields.Float()

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        current_uid = self._uid
        user = self.sudo().env['res.users'].browse(current_uid)
        defaults.setdefault('pos_id', user.pos_id.id)
        defaults.setdefault('date', date.today())

        if (user.pos_id.method_payment_id.payment_method_id.id != False):

            list = get_list_currency(
                user.pos_id.method_payment_id.payment_method_id.method_payment_currency_ids, self)

            defaults.setdefault(
                'account_payment_method_payment_bill_ids', list[0])

            defaults.setdefault(
                'account_payment_method_payment_coin_ids', list[1])

        return defaults

    @api.onchange('amount_cash_total',  'amount')
    def _calculation_diff_amount(self):
        for record in self:
            record.amount_diff = ((
                record.amount_cash_total)-record.amount)
            result_amount = record.amount_cash_total-record.amount_income
            if result_amount < 0:
                result_amount = 0
            record.amount_pos = result_amount

    @api.onchange('amount_income')
    def _calculation_income(self):
        for record in self:
            result_amount = record.amount_cash_total-record.amount_income
            if result_amount < 0:
                result_amount = 0
            record.amount_pos = result_amount

    @api.onchange('account_payment_method_payment_bill_ids', 'account_payment_method_payment_coin_ids')
    def _calculation_cash(self):
        for record in self:
            total = 0
            for val in record.account_payment_method_payment_bill_ids:
                val_number = val.number
                val_currency = val.method_payment_currency_id.value
                total = total+(val_number*val_currency)
            for val in record.account_payment_method_payment_coin_ids:
                val_number = val.number
                val_currency = val.method_payment_currency_id.value
                total = total+(val_number*val_currency)

            record.amount_cash_total = total

    def action_close_posted(self):
        for close in self:
            cid = close.env.company.id

            amount = close.amount_diff
            date = close.date
            pos_id = close.pos_id.id

            account_id_debit = close.pos_id.account_profit_loss_id.id
            account_id_credit = close.pos_id.account_id.id
            journal_id = close.pos_id.journal_close_id.id

            text = "Cierre de la caja : " + \
                close.pos_id.name+" dia : " + str(date)
            if (amount != 0):
                move = close.sudo().env["account.move"].create({
                    "company_id": cid,
                    "journal_id": journal_id,
                    "move_type": "entry",
                    "date": date,
                    "pos_id": pos_id,
                    "type": "cls",
                    "line_ids": [
                        Command.create({
                            "name": text,
                            "account_id": account_id_debit,
                            "debit": amount,
                        }),
                        Command.create({
                            "name": text,
                            "account_id": account_id_credit,
                            "credit": amount,
                        }),
                    ],
                })

                parameters = self.env['ir.config_parameter'].sudo()
                auto_posted_account_move = parameters.get_param(
                    'astore.auto_posted_account_move')
                if (auto_posted_account_move):
                    move.state = "posted"

                close.move_id = move
                close.sudo().env["aurb.astore.move.pos"].create({
                    "pos_id": pos_id,
                    "date": date,
                    "amount": amount,
                    "account_move_id": move.id,
                    "type": "cash",
                    "close_pos_id": close.id,
                    "closed": True,
                })

                amount_income = close.amount_income
                if (amount_income > 0):
                    type = "out"

                    account_id_income_debit = close.pos_id.account_income_id.id
                    account_id_income_credit = close.pos_id.account_id.id
                    move_income = close.sudo().env["account.move"].create({
                        "company_id": cid,
                        "journal_id": journal_id,
                        "move_type": "entry",
                        "date": date,
                        "pos_id": pos_id,
                        "type": "cls",
                        "line_ids": [
                            Command.create({
                                "name": text,
                                "account_id": account_id_income_debit,
                                "debit": amount_income,
                            }),
                            Command.create({
                                "name": text,
                                "account_id": account_id_income_credit,
                                "credit": amount_income,
                            }),
                        ],
                    })

                    parameters = self.env['ir.config_parameter'].sudo()
                    auto_posted_account_move = parameters.get_param(
                        'astore.auto_posted_account_move')
                    if (auto_posted_account_move):
                        move_income.state = "posted"

                    close.move_income_id = move_income

                    close.sudo().env["aurb.astore.move.pos"].create({
                        "pos_id": pos_id,
                        "date": date,
                        "amount": -amount_income,
                        "account_move_id": move_income.id,
                        "type": "cash",
                        "close_pos_id": close.id,
                        "closed": True,
                    })

                    close.sudo().env["aurb.astore.move.pos"].create({
                        "pos_id": pos_id,
                        "date": date,
                        "amount": (close.amount_cash_total)-amount_income,
                        "account_move_id": move_income.id,
                        "type": "cash",
                    })
                elif (amount_income <= 0):
                    close.sudo().env["aurb.astore.move.pos"].create({
                        "pos_id": pos_id,
                        "date": date,
                        "amount": close.amount_cash_total,
                        "account_move_id": move.id,
                        "type": "cash",
                        "closed": False,
                    })

            close.posted = True
            for move in close.move_ids:
                move.sudo().closed = True

        return True

    def action_close_load(self):
        for record in self:
            move_not_closed = self.sudo().env['aurb.astore.move.pos'].search([
                ('closed', '=', False),
                ('pos_id', '=', record.pos_id.id),
                ('date', '<=', record.date),
            ])
            record.amount_cash = 0
            record.amount_general = 0
            record.amount = 0

            browse_move = self.sudo().env["aurb.astore.move.pos"].browse(
                move_not_closed)
            for move in browse_move:
                if (move.id.account_move_id):
                    if (move.id.type == 'cash'):
                        record.amount_cash = record.amount_cash+move.id.amount
                        record.amount = record.amount + move.id.amount
                    elif (move.id.type == 'general'):
                        record.amount_general = record.amount_general+move.id.amount
                        record.amount = record.amount + move.id.amount
                else:
                    move.id.closed = True

            for move in browse_move:
                if (move.id.account_move_id):
                    move.id.close_pos_id = record

            if (record.pos_id.method_payment_id.payment_method_id.id != False):

                list = get_list_currency(
                    record.pos_id.method_payment_id.payment_method_id.method_payment_currency_ids, record)

                record.account_payment_method_payment_bill_ids = [(5, 0, 0)]
                record.account_payment_method_payment_bill_ids = list[0]

                record.account_payment_method_payment_coin_ids = [(5, 0, 0)]
                record.account_payment_method_payment_coin_ids = list[1]

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            view_name = record.pos_id.name+' '+str(record.date)
            record.display_name = view_name


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
