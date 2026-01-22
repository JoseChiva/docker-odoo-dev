from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

from datetime import timedelta, datetime

import csv
import locale


class FedorExportCron(models.Model):
    _name = 'fedor.export.cron'
    _description = 'Fedor export Cron'

    def export_file(self):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        log = self.sudo().env["fedor.export.import.log"].create({
            "name": "Ejecución proceso de Exportación %s" % date_time,
            "date_time": datetime.now(),
            "type": "export"
        })

        self.export_familia(log)
        self.export_articulo(log)
        self.export_clientes(log)
        self.export_tarifas(log)
        self.export_formas_de_pago(log)
        self.export_pedidos_pendientes(log)
        self.export_cobros_pendientes(log)

    def export_articulo(self, log):
        filename__ = 'i380232_articles.txt'
        file_path = get_module_resource('FEDOR', 'download/txt/', '')
        new_file_path = file_path.replace('\\', '/')
        # path_txt = new_file_path + '/' + filename__
        path_txt = 'tmp' + '/' + filename__

        locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')

        with open(path_txt, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            search_product = self.sudo().env['product.template'].search([
                ('detailed_type', '=', "product"),
                ('is_item_catalogue', '=', True),
            ])
            for product in search_product:
                codigo = product.default_code
                descripcion = product.with_context(lang='es_ES').name
                stock = product.qty_available
                barcode = product.barcode
                if (barcode == False):
                    barcode = ''
                familia = product.product_family_id.code
                type = product.type_id.code

                piezas_cajas = 1
                for pack in product.packaging_ids:
                    if (pack.sales == True):
                        # if (pack.name.lower() == "caja" and pack.sales == True):
                        piezas_cajas = pack.qty

                sale_minim_qty = 1
                if (product.sale_minim_qty != False):
                    sale_minim_qty = product.sale_minim_qty

                largo = 0
                ancho = 0
                alto = 0
                if (product.var1_s):
                    largo = product.var1_s
                if (product.var2_s):
                    ancho = product.var2_s
                if (product.var3_s):
                    alto = product.var3_s
                search_sale_order = self.sudo().env['sale.order.line'].search([
                    ('product_template_id', '=', product.id),
                    ('qty_to_deliver', '>', 0),
                    ('order_id.state', '!=', 'cancel'),
                ])
                qty_to_deliver = 0
                for line_pend in search_sale_order:
                    qty_to_deliver += line_pend.qty_to_deliver

                search_purchase_order = self.sudo().env['purchase.order.line'].search([
                    ('product_id', '=', product.id),
                    ('qty_to_invoice', '>', 0),
                ])
                date_planned = False
                qty_to_recived = 0

                for line_pend_recived in search_purchase_order:
                    qty_to_recived += line_pend_recived.qty_to_invoice
                    if (date_planned == False or date_planned > line_pend_recived.order_id.date_planned):
                        if (line_pend_recived.order_id):
                            date_planned = line_pend_recived.order_id.date_planned.strftime(
                                '%d/%m/%Y') if line_pend_recived.order_id.date_planned else ''

                if (date_planned == False):
                    date_planned = ""

                if (familia == False):
                    familia = ""

                if (type == False):
                    type = ""

                line = [
                    codigo,  # codigo
                    descripcion,  # descripcion
                    "",  # descripcion_2
                    "",  # descripcion_3
                    locale.format_string(
                        '%.3f', piezas_cajas, grouping=False),  # pzas/caja
                    locale.format_string(
                        '%.3f', stock, grouping=False),  # stock
                    locale.format_string(
                        '%.3f', qty_to_deliver, grouping=False),  # qty pendiente servir
                    locale.format_string(
                        '%.3f', qty_to_recived, grouping=False),  # qty pendiente recibir
                    date_planned,  # fecha_servicio
                    barcode,  # codigo_barras
                    "",  # ordenacion_1
                    "",  # ordenacion_2
                    locale.format_string(
                        '%.2f', sale_minim_qty, grouping=False),  # pzas_c_interior
                    locale.format_string(
                        '%.2f', largo, grouping=False),  # largo
                    locale.format_string(
                        '%.2f', ancho, grouping=False),  # ancho
                    locale.format_string(
                        '%.2f', alto, grouping=False),  # alto
                    "",  # dto oferta
                    "",  # largo caja
                    "",  # ancho caja
                    "",  # alto caja
                    familia,  # familia
                    type,  # tipo_articulo
                ]
                writer.writerow(line)

        log.add_line_text("Exportación de artículo correcta",
                          "", path_txt, filename__)

    def export_familia(self, log):
        filename__ = 'i380238_families.txt'
        file_path = get_module_resource('FEDOR', 'download/txt/', '')
        new_file_path = file_path.replace('\\', '/')
        # path_txt = new_file_path + '/' + filename__
        path_txt = 'tmp' + '/' + filename__

        with open(path_txt, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            text = ''
            # field = ["codigo", "descripcion"]
            # writer.writerow(field)
            search_family = self.sudo().env['fedor.product.family'].search([
                ('is_family_catalogue', '=', True)
            ])
            for family in search_family:
                line = [str(family.code),  # codigo
                        family.name  # descripcion
                        ]
                writer.writerow(line)

        log.add_line_text("Exportación de familia correcta",
                          "", path_txt, filename__)

    def export_clientes(self, log):
        filename__ = 'i380234_clients.txt'
        file_path = get_module_resource('FEDOR', 'download/txt/', '')
        new_file_path = file_path.replace('\\', '/')
        # path_txt = new_file_path + '/' + filename__
        path_txt = 'tmp' + '/' + filename__

        with open(path_txt, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            search_cliente = self.sudo().env['res.partner'].search([
                ('supplier_rank', '<', 1),
                ("is_company", "=", True),
                ("company_registry", "ilike", "43"),
            ])

            for cliente in search_cliente:
                any_direction = False

                # Añadimos las dirección basica del propio cliente, ya que en el caso de tener mas de una dirreccón
                # no se estaria exportando
                if (1 == 1):
                    user_id = cliente.referrer_id.company_registry
                    if (user_id == False):
                        user_id = ""

                    property_payment_term_id = cliente.property_payment_term_id.code
                    if (property_payment_term_id == False):
                        property_payment_term_id = cliente.property_payment_term_id.code
                        if (property_payment_term_id == False):
                            property_payment_term_id = ""

                    property_product_pricelist = cliente.property_product_pricelist.code
                    if (property_product_pricelist == False):
                        property_product_pricelist = cliente.property_product_pricelist.code
                        if (property_product_pricelist == False):
                            property_product_pricelist = ""

                    numero_recibos = 1
                    property_payment_term_ids = cliente.property_payment_term_id.line_ids
                    if (property_payment_term_ids == False):
                        property_payment_term_ids = cliente.property_payment_term_id.line_ids
                        if (property_payment_term_id == False):
                            numero_recibos = 0

                    first_interval = 0
                    other_interval = 0
                    for line in property_payment_term_ids:
                        if (first_interval == 0):
                            first_interval = line.nb_days
                        else:
                            other_interval = line.nb_days-first_interval

                        numero_recibos += 1

                    ccc1 = ""
                    ccc2 = ""
                    dc = ""
                    num_cuenta = ""
                    bank_ids = cliente.bank_ids
                    if (bank_ids != False):
                        for bank in bank_ids:
                            ccc1 = bank.acc_number[4: 8]
                            ccc2 = bank.acc_number[8: 12]
                            dc = bank.acc_number[12: 14]
                            num_cuenta = bank.acc_number[14: 24]

                    type = cliente.type_id.code
                    if (type == False):
                        type = cliente.type_id.code
                        if (type == False):
                            type = ""

                    commision = ""
                    property_product_pricelist_com = cliente.property_product_pricelist.id
                    if (property_product_pricelist_com == False):
                        property_product_pricelist_com = cliente.property_product_pricelist.id

                    search_commision = self.sudo().env['commission.rule'].search([
                        ('pricelist_id', '=', property_product_pricelist_com),
                    ])
                    for com in search_commision:
                        commision = com.rate

                    # if (property_payment_term_ids == False):
                    #     property_payment_term_ids = cliente.property_payment_term_id.line_ids
                    #     if (property_payment_term_id == False):
                    #         numero_recibos = 0
                    state = cliente.state_id.code
                    if (state == False):
                        state = ''
                    email = cliente.email
                    if (email == False):
                        email = ''

                    line = [cliente.company_registry,  # subcta
                            "1",  # orden
                            cliente.name,  # nombre
                            cliente.vat,  # dni
                            cliente.street,  # direccion
                            cliente.country_id.code,  # pais
                            state,  # provincia
                            cliente.zip,  # codigo_postal
                            cliente.city,  # poblacion
                            cliente.phone,  # telefono
                            email,  # email
                            property_payment_term_id,  # tipo_forma_pago
                            numero_recibos,  # numero recibos
                            first_interval,  # primer intervalo
                            other_interval,  # otros intervalos
                            "",  # dia pago 1
                            "",  # dia pago 2
                            ccc1,  # ccc1
                            ccc2,  # ccc2
                            dc,  # dc
                            num_cuenta,  # num cuenta
                            property_product_pricelist,  # tarifa
                            "",  # dto pp
                            "",  # dto1
                            "",  # dto2
                            "",  # dto3
                            user_id,  # vendedor
                            commision,  # comision
                            "9",  # moneda
                            "",  # tipo_iva
                            type,  # tipo_cliente
                            ]
                    writer.writerow(line)
                    any_direction = True

                for dic in cliente.child_ids:
                    if dic.type == 'delivery':
                        any_direction = True

                        user_id = dic.referrer_id.company_registry
                        if (user_id == False):
                            user_id = cliente.referrer_id.company_registry
                            if (user_id == False):
                                user_id = ""

                        property_payment_term_id = dic.property_payment_term_id.code
                        if (property_payment_term_id == False):
                            property_payment_term_id = cliente.property_payment_term_id.code
                            if (property_payment_term_id == False):
                                property_payment_term_id = ""

                        property_product_pricelist = dic.property_product_pricelist.code
                        if (property_product_pricelist == False):
                            property_product_pricelist = cliente.property_product_pricelist.code
                            if (property_product_pricelist == False):
                                property_product_pricelist = ""

                        numero_recibos = 1
                        property_payment_term_ids = dic.property_payment_term_id.line_ids
                        if (property_payment_term_ids == False):
                            property_payment_term_ids = cliente.property_payment_term_id.line_ids
                            if (property_payment_term_id == False):
                                numero_recibos = 0

                        first_interval = 0
                        other_interval = 0
                        for line in property_payment_term_ids:
                            if (first_interval == 0):
                                first_interval = line.nb_days
                            else:
                                other_interval = line.nb_days-first_interval

                            numero_recibos += 1

                        ccc1 = ""
                        ccc2 = ""
                        dc = ""
                        num_cuenta = ""
                        bank_ids = dic.bank_ids
                        if (bank_ids != False):
                            for bank in bank_ids:
                                ccc1 = bank.acc_number[4: 8]
                                ccc2 = bank.acc_number[8: 12]
                                dc = bank.acc_number[12: 14]
                                num_cuenta = bank.acc_number[14: 24]

                        type = dic.type_id.code
                        if (type == False):
                            type = cliente.type_id.code
                            if (type == False):
                                type = ""

                        commision = ""
                        property_product_pricelist_com = dic.property_product_pricelist.id
                        if (property_product_pricelist_com == False):
                            property_product_pricelist_com = cliente.property_product_pricelist.id

                        search_commision = self.sudo().env['commission.rule'].search([
                            ('pricelist_id', '=', property_product_pricelist_com),
                        ])
                        for com in search_commision:
                            commision = com.rate

                        # if (property_payment_term_ids == False):
                        #     property_payment_term_ids = cliente.property_payment_term_id.line_ids
                        #     if (property_payment_term_id == False):
                        #         numero_recibos = 0
                        state = dic.state_id.code
                        if (state == False):
                            state = ''
                        email = dic.email
                        if (email == False):
                            email = ''

                        line = [cliente.company_registry,  # subcta
                                dic.ref,  # orden
                                cliente.name,  # nombre
                                cliente.vat,  # dni
                                dic.street,  # direccion
                                dic.country_id.code,  # pais
                                state,  # provincia
                                dic.zip,  # codigo_postal
                                dic.city,  # poblacion
                                dic.phone,  # telefono
                                email,  # email
                                property_payment_term_id,  # tipo_forma_pago
                                numero_recibos,  # numero recibos
                                first_interval,  # primer intervalo
                                other_interval,  # otros intervalos
                                "",  # dia pago 1
                                "",  # dia pago 2
                                ccc1,  # ccc1
                                ccc2,  # ccc2
                                dc,  # dc
                                num_cuenta,  # num cuenta
                                property_product_pricelist,  # tarifa
                                "",  # dto pp
                                "",  # dto1
                                "",  # dto2
                                "",  # dto3
                                user_id,  # vendedor
                                commision,  # comision
                                "9",  # moneda
                                "",  # tipo_iva
                                type,  # tipo_cliente
                                ]
                        writer.writerow(line)
                if (any_direction == False):

                    user_id = cliente.referrer_id.company_registry
                    if (user_id == False):
                        user_id = ""

                    property_payment_term_id = cliente.property_payment_term_id.code
                    if (property_payment_term_id == False):
                        property_payment_term_id = ""

                    property_product_pricelist = cliente.property_product_pricelist.code

                    if (property_product_pricelist == False):
                        property_product_pricelist = ""

                    commision = ""
                    property_product_pricelist_com = cliente.property_product_pricelist.id
                    search_commision = self.sudo().env['commission.rule'].search([
                        ('pricelist_id', '=', property_product_pricelist_com),
                    ])
                    for com in search_commision:
                        commision = com.rate

                    numero_recibos = 1
                    property_payment_term_ids = cliente.property_payment_term_id.line_ids
                    if (property_payment_term_ids == False):
                        property_payment_term_ids = cliente.property_payment_term_id.line_ids
                        if (property_payment_term_id == False):
                            numero_recibos = 0

                    first_interval = 0
                    other_interval = 0
                    for line in property_payment_term_ids:
                        if (first_interval == 0):
                            first_interval = line.nb_days
                        else:
                            other_interval = line.nb_days-first_interval

                        numero_recibos += 1

                    ccc1 = ""
                    ccc2 = ""
                    dc = ""
                    num_cuenta = ""
                    bank_ids = cliente.bank_ids
                    if (bank_ids != False):
                        for bank in bank_ids:
                            ccc1 = bank.acc_number[4: 8]
                            ccc2 = bank.acc_number[8: 12]
                            dc = bank.acc_number[12: 14]
                            num_cuenta = bank.acc_number[14: 24]

                    type = cliente.type_id.code
                    if (type == False):
                        type = ""

                    state = cliente.state_id.code
                    if (state == False):
                        state = ''
                    email = cliente.email
                    if (email == False):
                        email = ''

                    line = [cliente.company_registry,  # subcta
                            "1",  # orden
                            cliente.name,  # nombre
                            cliente.vat,  # dni
                            cliente.street,  # direccion
                            cliente.country_id.code,  # pais
                            state,  # provincia
                            cliente.zip,  # codigo_postal
                            cliente.city,  # poblacion
                            cliente.phone,  # telefono
                            email,  # email
                            property_payment_term_id,  # tipo_forma_pago
                            numero_recibos,  # numero recibos
                            first_interval,  # primer intervalo
                            other_interval,  # otros intervalos
                            "",  # dia pago 1
                            "",  # dia pago 2
                            ccc1,  # ccc1
                            ccc2,  # ccc2
                            dc,  # dc
                            num_cuenta,  # num cuenta
                            property_product_pricelist,  # tarifa
                            "",  # dto pp
                            "",  # dto1
                            "",  # dto2
                            "",  # dto3
                            user_id,  # vendedor
                            commision,  # comision
                            "9",  # moneda
                            "",  # tipo_iva
                            type,  # tipo_cliente
                            ]
                    writer.writerow(line)

        # self.read_file(filename, "Exportación de clientes correcta", log)
        log.add_line_text("Exportación de clientes correcta",
                          "", path_txt, filename__)

    def export_tarifas(self, log):
        filename__ = 'i380233_tarifes.txt'
        file_path = get_module_resource('FEDOR', 'download/txt/', '')
        new_file_path = file_path.replace('\\', '/')
        # path_txt = new_file_path + '/' + filename__
        path_txt = 'tmp' + '/' + filename__

        with open(path_txt, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            search_product_list = self.sudo().env['product.pricelist'].search([
            ])
            for product_list in search_product_list:
                name = product_list.code
                for product in product_list.item_ids:

                    commision = ""
                    property_product_pricelist = product_list.id
                    search_commision = self.sudo().env['commission.rule'].search([
                        ('pricelist_id', '=', property_product_pricelist),
                    ])
                    for com in search_commision:
                        commision = com.rate

                    writer.writerow([product.product_tmpl_id.default_code,  # codigo
                                    name,  # tarifa
                                    str(product.fixed_price).replace(
                                        '.', ','),  # precio
                                    commision,  # comision
                                     ])
        log.add_line_text("Exportación de tarifa correcta",
                          "", path_txt, filename__)

    def export_formas_de_pago(self, log):
        filename__ = 'i380235_formas_de_pago.txt'
        file_path = get_module_resource('FEDOR', 'download/txt/', '')
        new_file_path = file_path.replace('\\', '/')
        # path_txt = new_file_path + '/' + filename__
        path_txt = 'tmp' + '/' + filename__

        with open(path_txt, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            search_account_payment_term = self.sudo().env['account.payment.term'].search([
            ])
            for payment_term in search_account_payment_term:
                writer.writerow([payment_term.code,  # forma pago
                                 "1",  # idioma
                                 payment_term.name  # descripcion
                                 ])
        log.add_line_text("Exportación de formas de pago correcta",
                          "", path_txt, filename__)

    def export_pedidos_pendientes(self, log):
        filename__ = 'i380236_comandes.txt'
        file_path = get_module_resource('FEDOR', 'download/txt/', '')
        new_file_path = file_path.replace('\\', '/')
        # path_txt = new_file_path + '/' + filename__
        path_txt = 'tmp' + '/' + filename__

        with open(path_txt, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            search_sale_order = self.sudo().env['sale.order'].search([
                ('invoice_status', '=', ['to invoice', 'no']),
            ])
            for sale_order in search_sale_order:
                for sale_order_line in sale_order.order_line:
                    if (sale_order_line.qty_to_invoice > 0):
                        writer.writerow([
                            sale_order.partner_id.company_registry,  # subcta
                            sale_order_line.product_template_id.default_code,  # codigo_art
                            sale_order_line.qty_to_invoice,  # qty
                            sale_order_line.price_unit,  # precio
                            sale_order.date_order.strftime(
                                '%d/%m/%Y') if sale_order.date_order else '',  # fecha_documento
                        ])
        log.add_line_text("Exportación de pedidos pendientes correcta",
                          "", path_txt, filename__)

    def export_cobros_pendientes(self, log):
        filename__ = 'i380237_cobraments.txt'
        file_path = get_module_resource('FEDOR', 'download/txt/', '')
        new_file_path = file_path.replace('\\', '/')
        # path_txt = new_file_path + '/' + filename__
        path_txt = 'tmp' + '/' + filename__

        with open(path_txt, 'w', newline='') as csvfile:

            writer = csv.writer(csvfile, delimiter=';')
            search_account_move = self.sudo().env['account.move'].search([
                ('state', '=', 'posted'),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', '<>', 'paid'),
            ])
            for account_move in search_account_move:
                writer.writerow([
                    account_move.partner_id.company_registry,  # subcta
                    account_move.name,  # documento
                    account_move.invoice_payment_term_id.name,  # tipo documento
                    account_move.invoice_date.strftime(
                        '%d/%m/%Y') if account_move.invoice_date else '',  # fecha emision
                    account_move.delivery_date.strftime(
                        '%d/%m/%Y') if account_move.delivery_date else '',  # fecha_vencimiento
                    account_move.amount_total,  # importe
                    9,  # moneda
                ])
            log.add_line_text("Exportación de cobros pendientes correcta",
                              "", path_txt, filename__)
