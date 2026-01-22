from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime

import csv
import io

import base64


class FedorImport(models.TransientModel):
    _name = 'fedor.import.order'
    _description = 'Fedor impoertación pedido'

    file_head = fields.Binary(
        attachment=True,
        string="Fichero de cabecera",
        copy=False,
    )
    text_file_head = fields.Char("File Name Head")

    file_line = fields.Binary(
        attachment=True,
        string="Fichero de líneas",
        copy=False,
    )
    text_file_line = fields.Char("File Name Line")

    def action_import_order(self):
        for reg in self:
            error_message_ = ""
            file_head = reg.file_head
            file_line = reg.file_line

            file_content_head = base64.decodebytes(file_head)

            file_content_head = file_content_head.decode("utf-8")
            orders = []
            error = False
            error_message_ += "CABECERA :"
            file_lines = file_content_head.split("\r\n")
            for line in file_lines:
                if (line != ''):
                    data = line.split(';')
                    if (len(data) < 7):
                        error = True
                        error_message_ += "\n"+"El fichero de cabecera no tiene el formato correcto"
                    else:
                        number = data[0]
                        search_sale_order = self.sudo().env['sale.order'].search([
                            ('origin', '=', number),
                        ])
                        for order in search_sale_order:
                            error = True
                            error_message_ += "\n"+"Se ha encontrado un documento con el numero : "+number

                        partner = data[1]
                        search_cliente = self.sudo().env['res.partner'].search([
                            ('customer_rank', '>', 0),
                            ('company_registry', '=', partner),
                            ('is_company', '=', True),
                        ])
                        partner_id = ""
                        disc_1 = 0
                        disc_2 = 0
                        disc_3 = 0
                        for part in search_cliente:
                            partner_id = part.id

                        if (partner_id == ""):
                            error = True
                            error_message_ += "\n"+"No se ha encontrado el cliente con código : " + \
                                partner+" numero de pedido : "+number

                        sales_person = data[2]
                        sales_person_id = ""
                        search_sales_person = self.sudo().env['res.partner'].search([
                            ('company_registry', '=', sales_person),
                            ('is_company', '=', True),
                            ('grade_id', '!=', False),
                        ])
                        for sale in search_sales_person:
                            sales_person_id = sale.id
                        if (sales_person_id == ""):
                            error = True
                            error_message_ += "\n"+"No se ha encontrado el representante con código : " + \
                                sales_person+" numero de pedido : "+number

                        date_order = data[3]
                        try:
                            date_order = datetime.strptime(
                                date_order, "%d/%m/%Y")
                        except ValueError:
                            error = True
                            error_message_ += "\n"+"Formato de fecha incorrecto : " + \
                                date_order+" numero de pedido : "+number

                        discount = data[4]

                        delivery_address = data[5]
                        delivery_address_id = ""
                        search_delivery_address = self.sudo().env['res.partner'].search([
                            ('ref', '=', delivery_address),
                            ('parent_id', '=', partner_id),
                        ])
                        for del_add in search_delivery_address:
                            delivery_address_id = del_add.id
                            partner_id = del_add.id
                        if (delivery_address_id == ""):
                            if (delivery_address != "1"):
                                error = True
                                error_message_ += "\n"+"No se ha encontrado la dirección con código : " + \
                                    delivery_address+" numero de pedido : "+number

                        payment_method = data[6]

                        comments = data[7]

                        orders.append(OrderHead(
                            number, partner_id, sales_person_id, date_order, payment_method, comments))

            file_content_line = base64.decodebytes(file_line)
            file_content_line = file_content_line.decode("utf-8")

            error_message_ += "\nLÍNEAS :"
            file_lines = file_content_line.split("\r\n")
            for line in file_lines:
                if (line != ''):
                    data = line.split(';')
                    if (len(data) < 5):
                        error = True
                        error_message_ += "\n"+"El fichero de líneas no tiene el formato correcto"
                    else:
                        number = data[0]
                        number_line = data[1]
                        item_code = data[2]
                        search_product = self.sudo().env['product.product'].search([
                            ('default_code', '=', item_code),
                        ])
                        item_id = ""
                        item_pack = ""
                        item_name = ""
                        auren_printed_line = False
                        uom_id = ""
                        for item in search_product:
                            item_id = item.id
                            item_name = item.name
                            uom_id = item.uom_id.id
                            auren_printed_line = item.auren_printed_line
                            if (item.packaging_ids):
                                item_pack = item.packaging_ids[0].id
                        if (item_id == ""):
                            error = True
                            error_message_ += "\n"+"No se ha encontrado en la línea " + \
                                number_line+" numero de pedido : "+number + \
                                " el artículo con código : "+item_code

                        quantity = data[3]
                        try:
                            float(quantity)
                        except ValueError:
                            error = True
                            error_message_ += "\n"+"Formato de cantidad incorrecto : " + \
                                quantity+" numero de pedido : "+number+" línea : "+number_line

                        price = data[4]
                        try:
                            float(price)
                        except ValueError:
                            error = True
                            error_message_ += "\n"+"Formato de price incorrecto : " + \
                                price+" numero de pedido : "+number+" línea : "+number_line

                        discount = data[5]
                        order_find = False
                        for order in orders:
                            if (order.number == number):
                                order_find = True
                                order.add_line(number, number_line,
                                               item_id, item_name, quantity, price, uom_id, item_pack, auren_printed_line, self)
                        if (order_find == False):
                            error = True
                            error_message_ += "\n"+"Numero de pedido no encontrado en cabecera " + \
                                number+" línea : "+number_line

            for order in orders:
                if (len(order.line) == 0):
                    error = True
                    error_message_ += "\n"+"El pedido numero : " + \
                        order.number + " no tiene líneas asociadas"

            if (error):
                raise ValidationError(
                    error_message_)

            now = datetime.now()  # current date and time
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

            log = self.sudo().env["fedor.export.import.log"].create({
                "name": "Ejecución proceso de importación %s" % date_time,
                "date_time": datetime.now(),
                "type": "import"
            })

            for order in orders:
                order.save(self, log)

            log.add_line_text_order("Importación de pedido cabecera correcta",
                                    "", file_head, reg.text_file_head)
            log.add_line_text_order("Importación de pedido líneas correcta",
                                    "", file_line, reg.text_file_line)


class OrderHead:

    def __init__(self, number, partner_id, sales_person, date_order, payment_method, comments):
        self.number = number
        self.partner_id = partner_id
        self.sales_person = sales_person
        self.date_order = date_order
        self.payment_method = payment_method
        self.comments = comments
        self.line = []

    def add_line(self, number, number_line, item_code, item_name, quantity, price, uom_id, item_pack, auren_printed_line, odoo):
        disc_lin_1 = 0
        disc_lin_2 = 0
        disc_lin_3 = 0
        if (self.partner_id != ''):
            search_cliente = odoo.sudo().env['res.partner'].search([
                ('id', '=', self.partner_id),
            ])

            for part in search_cliente:
                disc_lin_1 = part.disc_1
                disc_lin_2 = part.disc_2
                disc_lin_3 = part.disc_3

        order = OrderLine(number, number_line, item_code,
                          item_name, quantity, price, uom_id, item_pack, auren_printed_line, disc_lin_1, disc_lin_2, disc_lin_3)
        self.line.append(order)

    def save(self, odoo, log):

        add_lines = []
        sequence = 0
        line_env = odoo.sudo().env['sale.order.line']
        for lin in self.line:
            add_lines.append((0, 0, {
                # 'order_id': order_b.id,
                'product_id': lin.product_id,
                # 'product_uom': lin.uom_id,
                # 'name': lin.name,
                'price_unit': lin.price_unit,
                'product_uom_qty': lin.quantity,
                'product_packaging_id': lin.item_pack,
                'auren_printed_line': lin.auren_printed_line,
                'disc_1': lin.disc_1,
                'disc_2': lin.disc_2,
                'disc_3': lin.disc_3,
            }))
            sequence = sequence+1

        order_b = odoo.sudo().env["sale.order"].create({
            "partner_id": self.partner_id,
            "date_order": self.date_order,
            'order_line': add_lines,
            'origin': self.number,
            'referrer_id': self.sales_person,
            'note': self.comments,
        })
        if (order_b.partner_id.disc_head_1 != False):
            discount_percent = order_b.partner_id.disc_head_1/100
            order_b._create_update_discount_lines(
                discount_percent, "1", "disc_1", sequence+1, False, True)
        if (order_b.partner_id.disc_head_2 != False):
            discount_percent = order_b.partner_id.disc_head_2/100
            order_b._create_update_discount_lines(
                discount_percent, "2", "disc_2", sequence+1, False, True)
        if (order_b.partner_id.disc_head_3 != False):
            discount_percent = order_b.partner_id.disc_head_3/100
            order_b._create_update_discount_lines(
                discount_percent, "3", "disc_3", sequence+1, False, True)

        for line in order_b.order_line:
            line._change_discount()
            if (sequence < line.sequence):
                sequence = line.sequence
            if (line.type_disc == "disc_1"):
                disc_1 = line
            if (line.type_disc == "disc_2"):
                disc_2 = line
            if (line.type_disc == "disc_3"):
                disc_3 = line
            if (line.type_disc == "disc_4"):
                disc_4 = line
            if (line.type_disc == "disc_5"):
                disc_5 = line
            if (line.type_disc == "disc_6"):
                disc_6 = line

        if (order_b.partner_id.disc_head_1 != False):
            discount_percent = order_b.partner_id.disc_head_1/100
            order_b._create_update_discount_lines(
                discount_percent, "1", "disc_1", sequence+1, disc_1, True)
        if (order_b.partner_id.disc_head_2 != False):
            discount_percent = order_b.partner_id.disc_head_2/100
            order_b._create_update_discount_lines(
                discount_percent, "2", "disc_2", sequence+1, disc_2, True)
        if (order_b.partner_id.disc_head_3 != False):
            discount_percent = order_b.partner_id.disc_head_3/100
            order_b._create_update_discount_lines(
                discount_percent, "3", "disc_3", sequence+1, disc_3, True)

        log .add_line_order(order_b.id)


class OrderLine:
    def __init__(self, number, number_line, product_id, name, quantity, price_unit, uom_id, item_pack, auren_printed_line, disc_1, disc_2, disc_3):
        self.number = number
        self.number_line = number_line
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price_unit = price_unit
        self.uom_id = uom_id
        self.item_pack = item_pack
        self.auren_printed_line = auren_printed_line
        self.disc_1 = disc_1
        self.disc_2 = disc_2
        self.disc_3 = disc_3
