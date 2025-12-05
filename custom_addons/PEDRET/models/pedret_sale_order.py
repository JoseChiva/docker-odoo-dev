from odoo import fields, models
from ast import literal_eval
from odoo.osv import expression


class PedretSaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[(
        'llibreta', 'Llibreta'),])

    def action_llibreta(self):
        for sale_order in self:
            sale_order.state = "llibreta"
            if ("L" not in sale_order.name):
                sale_order.name = sale_order.name.replace("S", "L")

    def action_to_draft(self):
        for sale_order in self:
            sale_order.state = "draft"

    # def _compute_get_aprroval(self):
    #     for order in self:
    #         order.approval_count = len(order.approval_request_ids)

    # def _compute_get_aprroval_status(self):
    #     for order in self:
    #         if (order.approval_request_ids):
    #             for approval in order.approval_request_ids:
    #                 order.approval_status = approval.request_status
    #         else:
    #             order.approval_status = False

    # def button_approve(self):
    #     self.action_confirm()

    # def action_quotation_send(self):
    #     state = self.state
    #     active_approval = self.validate_aprroval_quotation()
    #     if (active_approval):
    #         return
    #     dev = super(SaleOrder, self).action_quotation_send()
    #     if (state == "approved"):
    #         self.state = "approved"
    #     return dev

    # def action_confirm(self):
    #     active_approval = self.validate_aprroval_quotation()
    #     if (active_approval):
    #         return
    #     return super(SaleOrder, self).action_confirm()

    # # def action_cancel(self):
    # #     self.state = 'cancel'

    # def validate_aprroval_quotation(self):
    #     for order in self:
    #         if (order.team_id):
    #             active_system_approval = False
    #             if (order.state != 'approved'):
    #                 category_id = order.team_id.approval_category_id
    #                 if (category_id):
    #                     text_aprroval = order.custom_validate_approval()
    #                     if (text_aprroval):
    #                         active_system_approval = True

    #                     domain = order.team_id.rule_approved_domain
    #                     domain = literal_eval(domain or '[]')
    #                     if domain:
    #                         end_domain = expression.AND(
    #                             [domain, [('id', '=', order.id)]])
    #                         sale_order_find = self.env['sale.order'].search(
    #                             end_domain, limit=1)
    #                         if (sale_order_find):
    #                             text_aprroval += ", " + order.team_id.text_aprroval
    #                             active_system_approval = True
    #             else:
    #                 order.state = 'draft'
    #                 order.locked = False

    #             if (active_system_approval):
    #                 order.state = 'to_approve'
    #                 order.locked = True
    #                 order.create_approval(
    #                     category_id, text_aprroval)
    #                 # if (approval_request):
    #                 #     order.approval_request_id = approval_request

    #                 return True
    #     return False

    # def create_approval(order, category_id, text_aprroval):

    #     approval_request = order.sudo().env["approval.request"].create({
    #         "name": 'Sale Order aprrove : '+order.name,
    #         'request_owner_id': order.user_id.id,
    #         "category_id": category_id.id,
    #         "date": order.date_order,
    #         'reason': text_aprroval,
    #         'order_id': order.id,
    #     })
    #     approval_request.sudo().action_confirm()

    # def custom_validate_approval(order):
    #     for line in order.order_line:
    #         if (line.product_id.list_price != line.price_unit):
    #             return "The order price can't lesser than the sale price"
    #     return ""
