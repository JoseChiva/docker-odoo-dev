from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _
from collections import defaultdict


class AurenSaleAccountMoveLine(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        invoices = super().create(vals)

        for invoice in invoices:
            if (invoice.move_type == "out_invoice"):
                for invoice_line in invoice.invoice_line_ids:
                    if (invoice_line.sale_line_ids):
                        invoice_line.type_disc = invoice_line.sale_line_ids[0].type_disc
                        invoice_line.disc_1 = invoice_line.sale_line_ids[0].disc_1
                        invoice_line.disc_2 = invoice_line.sale_line_ids[0].disc_2
                        invoice_line.disc_3 = invoice_line.sale_line_ids[0].disc_3
                        invoice_line.disc_4 = invoice_line.sale_line_ids[0].disc_4
                        invoice_line.disc_5 = invoice_line.sale_line_ids[0].disc_5
                        invoice_line.disc_6 = invoice_line.sale_line_ids[0].disc_6
                invoice._add_update_discount_head(False)
        return invoices

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form':
            parameters = self.env['ir.config_parameter'].sudo()

            group_extended_discount = self.env.user.has_group(
                'multi_discount_sale.group_extended_discount')
            if (group_extended_discount):
                for node in arch.xpath(
                    "//field[@name='discount']"
                ):
                    node.attrib['optional'] = "hide"
            var_readonly = parameters.get_param(
                'multi_discount_sale.var_readonly_s')

            name_var1 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_1')
            if (name_var1 != False):
                for node in arch.xpath(
                    "//field[@name='disc_1']"
                ):
                    node.attrib['string'] = name_var1

            name_var2 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_2')
            if (name_var2 != False):
                for node in arch.xpath(
                    "//field[@name='disc_2']"
                ):
                    node.attrib['string'] = name_var2

            name_var3 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_3')
            if (name_var3 != False):
                for node in arch.xpath(
                    "//field[@name='disc_3']"
                ):
                    node.attrib['string'] = name_var3

            name_var4 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_4')
            if (name_var4 != False):
                for node in arch.xpath(
                    "//field[@name='disc_4']"
                ):
                    node.attrib['string'] = name_var4

            name_var5 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_5')
            if (name_var5 != False):
                for node in arch.xpath(
                    "//field[@name='disc_5']"
                ):
                    node.attrib['string'] = name_var5

            name_var6 = parameters.get_param(
                'multi_discount_sale.desc_group_extended_discount_6')
            if (name_var6 != False):
                for node in arch.xpath(
                    "//field[@name='disc_6']"
                ):
                    node.attrib['string'] = name_var6

        return arch, view

    @api.onchange('partner_id')
    def _multi_discount_sale_change_partner_id(self):
        self._add_update_discount_head(True)

    @api.onchange('invoice_line_ids')
    def _multi_discount_sale_change_order_line(self):
        self._add_update_discount_head(False)

    def _add_update_discount_head(self, create_line):

        parameters = self.env['ir.config_parameter'].sudo()
        group_extended_discount = self.env.user.has_group(
            'multi_discount_sale.group_head_extended_discount')

        if (group_extended_discount):

            disc_1 = False
            disc_2 = False
            disc_3 = False
            disc_4 = False
            disc_5 = False
            disc_6 = False

            for invoice in self:
                sequence = invoice.buscarultimalinea()

                tiene_disc_1 = invoice.tienedescuentopedido("disc_1")
                tiene_disc_2 = invoice.tienedescuentopedido("disc_2")
                tiene_disc_3 = invoice.tienedescuentopedido("disc_3")
                tiene_disc_4 = invoice.tienedescuentopedido("disc_4")
                tiene_disc_5 = invoice.tienedescuentopedido("disc_5")
                tiene_disc_6 = invoice.tienedescuentopedido("disc_6")

                disc_1 = invoice.buscarlineadescuento("disc_1")
                disc_2 = invoice.buscarlineadescuento("disc_2")
                disc_3 = invoice.buscarlineadescuento("disc_3")
                disc_4 = invoice.buscarlineadescuento("disc_4")
                disc_5 = invoice.buscarlineadescuento("disc_5")
                disc_6 = invoice.buscarlineadescuento("disc_6")

                if (tiene_disc_1 == True):
                    discount_percent = invoice.partner_id.disc_head_1/100
                    if (disc_1 == False):
                        invoice._create_update_discount_lines(
                            discount_percent, "1", "disc_1", sequence+1, disc_1, True)
                        disc_1 = invoice.buscarlineadescuento("disc_1")
                    invoice._create_update_discount_lines(
                        discount_percent, "1", "disc_1", sequence+1, disc_1, create_line)

                if (tiene_disc_2 == True):
                    discount_percent = invoice.partner_id.disc_head_2/100
                    if (disc_2 == False):
                        invoice._create_update_discount_lines(
                            discount_percent, "2", "disc_2", sequence+1, disc_2, True)
                        disc_2 = invoice.buscarlineadescuento("disc_2")
                    invoice._create_update_discount_lines(
                        discount_percent, "2", "disc_2", sequence+1, disc_2, create_line)
                if (tiene_disc_3 == True):
                    discount_percent = invoice.partner_id.disc_head_3/100
                    if (disc_3 == False):
                        invoice._create_update_discount_lines(
                            discount_percent, "3", "disc_3", sequence+1, disc_3, True)
                        disc_3 = invoice.buscarlineadescuento("disc_3")
                    invoice._create_update_discount_lines(
                        discount_percent, "3", "disc_3", sequence+1, disc_3, create_line)

                if (tiene_disc_4 == True):
                    discount_percent = invoice.partner_id.disc_head_4/100
                    if (disc_4 == False):
                        invoice._create_update_discount_lines(
                            discount_percent, "4", "disc_4", sequence+1, disc_4, True)
                        disc_4 = invoice.buscarlineadescuento("disc_4")
                    invoice._create_update_discount_lines(
                        discount_percent, "4", "disc_4", sequence+1, disc_4, create_line)
                if (tiene_disc_5 == True):
                    discount_percent = invoice.partner_id.disc_head_5/100
                    if (disc_5 == False):
                        invoice._create_update_discount_lines(
                            discount_percent, "5", "disc_5", sequence+1, disc_5, True)
                        disc_5 = invoice.buscarlineadescuento("disc_5")
                    invoice._create_update_discount_lines(
                        discount_percent, "5", "disc_5", sequence+1, disc_5, create_line)
                if (tiene_disc_6 == True):
                    discount_percent = invoice.partner_id.disc_head_6/100
                    if (disc_6 == False):
                        invoice._create_update_discount_lines(
                            discount_percent, "6", "disc_6", sequence+1, disc_6, True)
                        disc_6 = invoice.buscarlineadescuento("disc_6")
                    invoice._create_update_discount_lines(
                        discount_percent, "6", "disc_6", sequence+1, disc_6, create_line)

    def tienedescuentopedido(self, type_disc):
        tienedescuento = False
        if (len(self.invoice_line_ids) > 0):
            if (self.invoice_line_ids[0].sale_line_ids):
                for line_order in self.invoice_line_ids[0].sale_line_ids.order_id.order_line:
                    if (type_disc == line_order.type_disc):
                        tienedescuento = True
            else:
                if (type_disc == "disc_1"):
                    if (self.partner_id.disc_head_1):
                        tienedescuento = True
                elif (type_disc == "disc_2"):
                    if (self.partner_id.disc_head_2):
                        tienedescuento = True
                elif (type_disc == "disc_3"):
                    if (self.partner_id.disc_head_3):
                        tienedescuento = True
                elif (type_disc == "disc_4"):
                    if (self.partner_id.disc_head_4):
                        tienedescuento = True
                elif (type_disc == "disc_5"):
                    if (self.partner_id.disc_head_5):
                        tienedescuento = True
                elif (type_disc == "disc_6"):
                    if (self.partner_id.disc_head_6):
                        tienedescuento = True
        else:
            if (type_disc == "disc_1"):
                if (self.partner_id.disc_head_1):
                    tienedescuento = True
            elif (type_disc == "disc_2"):
                if (self.partner_id.disc_head_2):
                    tienedescuento = True
            elif (type_disc == "disc_3"):
                if (self.partner_id.disc_head_3):
                    tienedescuento = True
            elif (type_disc == "disc_4"):
                if (self.partner_id.disc_head_4):
                    tienedescuento = True
            elif (type_disc == "disc_5"):
                if (self.partner_id.disc_head_5):
                    tienedescuento = True
            elif (type_disc == "disc_6"):
                if (self.partner_id.disc_head_6):
                    tienedescuento = True

        return tienedescuento

    def buscarlineadescuento(self, type_disc):
        lin = False
        for line_invoice in self.invoice_line_ids:
            if (line_invoice.type_disc == type_disc):
                lin = line_invoice
        return lin

    def buscarultimalinea(self):
        sequence = 0
        for line_invoice in self.invoice_line_ids:
            if (sequence < line_invoice.sequence):
                sequence = line_invoice.sequence
        return sequence

    def _create_update_discount_lines(self, discount_percentage, number_disc, type_disc, sequence, line_disc, create_line):
        self.ensure_one()
        parameters = self.env['ir.config_parameter'].sudo()
        action_disc = parameters.get_param(
            'multi_discount_sale.operation_head_discount'+number_disc)
        desc_disc = parameters.get_param(
            'multi_discount_sale.desc_group_head_extended_discount_'+number_disc)
        discount_product = parameters.get_param(
            'multi_discount_sale.product_discount_'+number_disc+'_id')

        add_vat_line_discount = parameters.get_param(
            'multi_discount_sale.add_vat_line_discount')
        group_head_extended_discount_num = self.env.user.has_group(
            'multi_discount_sale.group_head_extended_discount_'+number_disc)
        sub_total_order = self._get_total(type_disc)
        if (line_disc != False):
            for taxes, subtotal in sub_total_order.items():
                imp_sub = 0
                if (action_disc == "dec"):
                    imp_sub = -subtotal
                else:
                    imp_sub = subtotal
                line_disc.price_unit = imp_sub*discount_percentage
                line_disc.sequence = sequence+1
                if (add_vat_line_discount):
                    line_disc.tax_ids = taxes.ids
        else:

            if (create_line):
                if (group_head_extended_discount_num):
                    # product_id = self.sudo().env['product.template'].browse(
                    #     int(discount_product))
                    product_id = self.sudo().env['product.product'].browse(
                        int(discount_product))

                    if (product_id != False):

                        vals_list = []
                        vals_list.append((0, 0, self._prepare_discount_line_values(
                            product=product_id,
                            amount=0,
                            taxes=False,
                            type_disc=type_disc, action_disc=action_disc, sequence=sequence,
                            description=_(
                                "%(desc_disc)s: %(percent)s%% ",
                                percent=discount_percentage*100,
                                desc_disc=desc_disc,
                            ),
                        )))
                        # for taxes, subtotal in sub_total_order.items():
                        #     vals_list.append((0, 0, self._prepare_discount_line_values(
                        #         product=product_id,
                        #         amount=subtotal * discount_percentage,
                        #         taxes=taxes,
                        #         type_disc=type_disc, action_disc=action_disc, sequence=sequence,
                        #         description=_(
                        #             "%(desc_disc)s: %(percent)s%% - On products with the following taxes %(taxes)s",
                        #             percent=discount_percentage*100,
                        #             taxes=", ".join(taxes.mapped('name')),
                        #             desc_disc=desc_disc,
                        #         ),
                        #     )))

                        self.invoice_line_ids = vals_list
                    # return self.sudo().env['sale.order.line'].create(vals_list)

    def _get_total(self, type_desc):
        total_price_per_tax_groups = defaultdict(float)
        for line in self.invoice_line_ids:
            if not line.quantity or not line.price_unit:
                continue
            if (line.type_disc == False):
                total_price_per_tax_groups[line.tax_ids] += line.price_subtotal
            else:
                if (line.type_disc[5:6] < type_desc[5:6]):
                    total_price_per_tax_groups[line.tax_ids] += line.price_subtotal
        return total_price_per_tax_groups

    def _prepare_discount_line_values(self, product, amount, taxes, type_disc, action_disc, sequence, description=None):
        self.ensure_one()
        imp = 0
        if (action_disc == "dec"):
            imp = -amount
        else:
            imp = amount
        if (taxes == False):
            vals = {
                'product_id': product.id,
                'quantity': 1,
                'sequence': sequence,
                'move_id': self.id,
                'price_unit': imp,
                'type_disc': type_disc,
            }
        else:
            vals = {
                'product_id': product.id,
                'quantity': 1,
                'sequence': sequence,
                'move_id': self.id,
                'price_unit': imp,
                'tax_ids': taxes.ids,
                'type_disc': type_disc,
            }

        if description:
            vals['name'] = description

        return vals
