import logging
from odoo import models, _, fields
from odoo.exceptions import UserError
import base64
from lxml import etree
from datetime import datetime
import re

_logger = logging.getLogger(__name__)


class SucoAccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    def action_financiada(self):
        """Genera un fichero PAIN.008 de remesa al descuento (prefijo FSDD), lo adjunta
        al `account.batch.payment`, publica un mensaje y marca el lote como 'financiada'.

        Reglas principales implementadas:
        - Agrupa las líneas por `invoice.invoice_date_due`.
        - Usa `payment.name` como `<EndToEndId>`.
        - Extrae `MndtId` y `DtOfSgntr` del modelo `sdd.mandate` (si existe) relacionado con
            el `res.partner` del deudor.
        - Adjunta el XML como `ir.attachment` y publica el mensaje en el hilo del lote.
        - Cambia el estado a `financiada` y oculta el botón si ya está en ese estado.
        """
        for rec in self:
            if rec.state == 'sent':
                raise UserError(_('El lote ya está marcado como Enviado.'))

            # Obtener pagos del lote: soportar distintos esquemas de relación
            payments = rec.mapped('payment_ids') if 'payment_ids' in rec._fields else self.env['account.payment'].search([('batch_id', '=', rec.id)])
            if not payments:
                raise UserError(_('No se han encontrado pagos asociados al lote.'))

            # Construir items por pago e invoice
            items = []
            mapping_list = []
            for pay in payments:
                # Obtener facturas relacionadas
                invoices = pay.invoice_ids if 'invoice_ids' in pay._fields else self.env['account.move'].search([('payment_id', '=', pay.id)])
                if not invoices:
                    # si no hay facturas, intentamos usar la información del propio pago
                    invoices = self.env['account.move']
                # por cada invoice tomamos una entrada (si hay varias, generamos varias entradas)
                for inv in invoices:
                    # Determinar fecha de vencimiento:
                    # Preferir invoice.invoice_date_due, luego date_maturity, luego invoice_date, luego payment.payment_date como fallback
                    due = None
                    if 'invoice_date_due' in inv._fields and inv.invoice_date_due:
                        due = inv.invoice_date_due
                        due_source = 'invoice.invoice_date_due'
                    elif 'date_maturity' in inv._fields and getattr(inv, 'date_maturity', False):
                        due = inv.date_maturity
                        due_source = 'invoice.date_maturity'
                    elif 'invoice_date' in inv._fields and getattr(inv, 'invoice_date', False):
                        due = inv.invoice_date
                        due_source = 'invoice.invoice_date'
                    else:
                        due = pay.payment_date if 'payment_date' in pay._fields and getattr(pay, 'payment_date', False) else fields.Date.context_today(self)
                        due_source = 'payment.payment_date_or_today'

                    # Mandato
                    mandate = None
                    try:
                        mandate = self.env['sdd.mandate'].search([('partner_id', '=', pay.partner_id.id)], limit=1)
                    except Exception:
                        mandate = None
                    # Banco/deudor
                    iban = ''
                    bic = ''
                    try:
                        if 'partner_bank_id' in pay._fields and pay.partner_bank_id:
                            iban = pay.partner_bank_id.acc_number or ''
                            bic = pay.partner_bank_id.bank_bic or ''
                        else:
                            # intentar partner bank
                            bank = pay.partner_id.bank_ids and pay.partner_id.bank_ids[0] or None
                            if bank:
                                iban = bank.acc_number or ''
                                bic = bank.bank_bic or ''
                    except Exception:
                        iban = ''
                        bic = ''

                    items.append({
                        'payment': pay,
                        'invoice': inv if inv and inv.exists() else None,
                        'due_date': due,
                        'end_to_end': pay.name,
                        'amount': float((inv.amount_total if inv and 'amount_total' in inv._fields and inv.amount_total is not None else pay.amount) or 0.0),
                        'mandate_id': (mandate.name if mandate else ''),
                        'mandate_date': (mandate.start_date if mandate and 'start_date' in mandate._fields else ''),
                        'debtor_iban': iban,
                        'debtor_bic': bic,
                    })

                    # Registro para depuración: payment -> due (incluir invoice y fuente)
                    mapping_list.append(f"{pay.name}:invoice={inv.name or inv.id}, due={str(due)}, src={due_source}")

            if not items:
                raise UserError(_('No hay líneas válidas para generar el fichero XML.'))

            # Registrar mapeo para ayudar en la depuración (payment_name:due_date) en logs
            if mapping_list:
                _logger.info("Mapeo pago→vencimiento: %s", ', '.join(mapping_list))

            # Agrupar por fecha de vencimiento (normalizar a YYYY-MM-DD)
            from datetime import date, datetime as _datetime
            grouped = {}
            for it in items:
                due = it['due_date']
                if isinstance(due, _datetime):
                    due = due.date()
                if isinstance(due, date):
                    key = due.isoformat()
                else:
                    key = str(due)
                grouped.setdefault(key, []).append(it)

            # Intentar obtener MsgId original desde un attachment existente para reutilizarlo
            base_msg = None
            atts = self.env['ir.attachment'].search([('res_model', '=', 'account.batch.payment'), ('res_id', '=', rec.id)])
            for att in atts:
                try:
                    data = att.datas and base64.b64decode(att.datas) or b''
                    if b'<MsgId>' in data:
                        txt = data.decode('utf-8')
                        start = txt.find('<MsgId>') + len('<MsgId>')
                        end = txt.find('</MsgId>', start)
                        if start and end:
                            base_msg = txt[start:end]
                            break
                except Exception:
                    continue
            if not base_msg:
                # Use the same MsgId approach as standard SDD exports (time-based unique id)
                import time
                base_msg = str(time.time())

            fsdd_msg = 'FSDD' + base_msg

            # Registrar claves de grupo detectadas y detalle por grupo en logs
            group_summary = ', '.join([f"{k}: {len(v)} txs, {sum(it['amount'] for it in v):.2f} EUR" for k, v in grouped.items()])
            _logger.info("Grupos detectados: %s", group_summary)
            # Registrar detalle de pagos por grupo para depuración
            groups_detail = []
            for k, v in sorted(grouped.items()):
                payments_detail = '; '.join([f"{itm['end_to_end']}({itm['amount']:.2f})" for itm in v])
                groups_detail.append(f"{k}: {payments_detail}")
            if groups_detail:
                _logger.info("Detalle por grupo: %s", ', '.join(groups_detail))

            # Construir XML
            NS = 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.02'
            NSMAP = {None: NS, 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
            root = etree.Element('Document', nsmap=NSMAP)
            cst = etree.SubElement(root, 'CstmrDrctDbtInitn')
            # GrpHdr
            grp = etree.SubElement(cst, 'GrpHdr')
            etree.SubElement(grp, 'MsgId').text = fsdd_msg
            etree.SubElement(grp, 'CreDtTm').text = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            total_txs = sum(len(v) for v in grouped.values())
            total_sum = sum(sum(it['amount'] for it in v) for v in grouped.values())
            etree.SubElement(grp, 'NbOfTxs').text = str(total_txs)
            etree.SubElement(grp, 'CtrlSum').text = ('%.2f' % total_sum)

            # InitgPty (datos del acreedor: usar company)
            company = rec.company_id or self.env.company
            init = etree.SubElement(grp, 'InitgPty')
            etree.SubElement(init, 'Nm').text = company.name
            id_el = etree.SubElement(init, 'Id')
            org = etree.SubElement(id_el, 'OrgId')
            oth = etree.SubElement(org, 'Othr')
            # Intentar obtener identificador acreedor (preferir sdd_creditor_identifier > VAT)
            creditor_id = company.sdd_creditor_identifier or company.vat or (company.partner_id and company.partner_id.vat) or ''
            etree.SubElement(oth, 'Id').text = creditor_id

            # PmtInf por vencimiento
            pmt_index = 0
            for due_key, lines in sorted(grouped.items()):
                pmt = etree.SubElement(cst, 'PmtInf')
                etree.SubElement(pmt, 'PmtInfId').text = f"{fsdd_msg}/{pmt_index}"
                etree.SubElement(pmt, 'PmtMtd').text = 'DD'
                etree.SubElement(pmt, 'BtchBookg').text = 'true'
                etree.SubElement(pmt, 'NbOfTxs').text = str(len(lines))
                sum_group = sum(it['amount'] for it in lines)
                etree.SubElement(pmt, 'CtrlSum').text = ('%.2f' % sum_group)

                # PmtTpInf
                pmttp = etree.SubElement(pmt, 'PmtTpInf')
                svc = etree.SubElement(pmttp, 'SvcLvl')
                etree.SubElement(svc, 'Cd').text = 'SEPA'
                lcl = etree.SubElement(pmttp, 'LclInstrm')
                # Use SDD scheme from mandate if available (mirrors account.payment behavior)
                try:
                    sdd_scheme = lines[0]['payment'].sdd_mandate_id.sdd_scheme or 'CORE'
                except Exception:
                    sdd_scheme = 'CORE'
                etree.SubElement(lcl, 'Cd').text = sdd_scheme
                etree.SubElement(pmttp, 'SeqTp').text = 'RCUR'

                # ReqdColltnDt (fecha de vencimiento)
                etree.SubElement(pmt, 'ReqdColltnDt').text = due_key

                # Creditor info (company)
                cdt = etree.SubElement(pmt, 'Cdtr')
                etree.SubElement(cdt, 'Nm').text = company.name
                cdtacct = etree.SubElement(pmt, 'CdtrAcct')
                idacc = etree.SubElement(cdtacct, 'Id')
                # Company IBAN
                comp_bank = company.partner_id.bank_ids and company.partner_id.bank_ids[0] or None
                comp_iban = getattr(comp_bank, 'sanitized_acc_number', None) or getattr(comp_bank, 'acc_number', '') if comp_bank else ''
                # Remove whitespace from IBAN for XML
                comp_iban = re.sub(r'\s+', '', comp_iban or '')
                etree.SubElement(idacc, 'IBAN').text = comp_iban
                cdtagt = etree.SubElement(pmt, 'CdtrAgt')
                fin = etree.SubElement(cdtagt, 'FinInstnId')
                comp_bic = getattr(comp_bank, 'bank_bic', '') if comp_bank else ''
                etree.SubElement(fin, 'BIC').text = comp_bic

                # CdtrSchmeId
                cdtsch = etree.SubElement(pmt, 'CdtrSchmeId')
                idsch = etree.SubElement(cdtsch, 'Id')
                prvt = etree.SubElement(idsch, 'PrvtId')
                oth2 = etree.SubElement(prvt, 'Othr')
                # Use creditor_id (preferred sdd_creditor_identifier or VAT) as set in the header
                etree.SubElement(oth2, 'Id').text = creditor_id or ''
                schm = etree.SubElement(oth2, 'SchmeNm')
                etree.SubElement(schm, 'Prtry').text = 'SEPA'

                # Lines
                for it in lines:
                    drct = etree.SubElement(pmt, 'DrctDbtTxInf')
                    pmtid = etree.SubElement(drct, 'PmtId')
                    etree.SubElement(pmtid, 'EndToEndId').text = it['end_to_end']
                    currency = getattr(it['payment'], 'currency_id', None)
                    currency_code = currency and currency.name or 'EUR'
                    etree.SubElement(drct, 'InstdAmt', Ccy=currency_code).text = ('%.2f' % it['amount'])
                    # Mandate
                    drctdbt = etree.SubElement(drct, 'DrctDbtTx')
                    mnd = etree.SubElement(drctdbt, 'MndtRltdInf')
                    etree.SubElement(mnd, 'MndtId').text = it['mandate_id'] or ''
                    etree.SubElement(mnd, 'DtOfSgntr').text = (it['mandate_date'] and fields.Date.to_string(it['mandate_date'])) or ''
                    # Debtor agent
                    dbagt = etree.SubElement(drct, 'DbtrAgt')
                    fininst = etree.SubElement(dbagt, 'FinInstnId')
                    etree.SubElement(fininst, 'BIC').text = it['debtor_bic'] or ''
                    # Debtor
                    dbtr = etree.SubElement(drct, 'Dbtr')
                    etree.SubElement(dbtr, 'Nm').text = it['payment'].partner_id.name or ''
                    addr = etree.SubElement(dbtr, 'PstlAdr')
                    etree.SubElement(addr, 'Ctry').text = (it['payment'].partner_id.country_id.code if it['payment'].partner_id.country_id else '') or ''
                    # simple address line
                    etree.SubElement(addr, 'AdrLine').text = (it['payment'].partner_id.contact_address or '')
                    # Debtor account
                    dbacct = etree.SubElement(drct, 'DbtrAcct')
                    iddb = etree.SubElement(dbacct, 'Id')
                    debtor_iban = re.sub(r'\s+', '', it['debtor_iban'] or '')
                    etree.SubElement(iddb, 'IBAN').text = debtor_iban
                    # RmtInf
                    rmt = etree.SubElement(drct, 'RmtInf')
                    ustrd = it['invoice'] and (it['invoice'].name or it['invoice'].narration or '') or (getattr(it['payment'], 'memo', None) or getattr(it['payment'], 'communication', None) or '')
                    etree.SubElement(rmt, 'Ustrd').text = ustrd

                pmt_index += 1

            # Serializar
            xml_bytes = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')

            # Crear attachment
            # Nombre de fichero que incluye el MsgId (fsdd_msg) para trazabilidad
            fname = f"{fsdd_msg}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.xml"
            attachment = self.env['ir.attachment'].create({
                'name': fname,
                'datas': base64.b64encode(xml_bytes),
                'res_model': 'account.batch.payment',
                'res_id': rec.id,
                'mimetype': 'application/xml',
            })

            # Publicar resumen y adjunto
            summary = _("Fichero PAIN.008 de descuento generado y adjuntado. Grupos por vencimiento: %s") % (', '.join([f"{k}: {len(v)} txs, {sum(it['amount'] for it in v):.2f} EUR" for k, v in grouped.items()]))
            rec.message_post(body=summary, attachment_ids=[attachment.id])

            # Marcar como enviado (comportamiento estándar) y terminar (usar sudo para evitar restricciones de escritura)
            rec.sudo().write({'state': 'sent'})

        # Recargar la vista para que el botón desaparezca del formulario
        return {'type': 'ir.actions.client', 'tag': 'reload'}
