'''
    empresa smallint NOT NULL,
    ejercicio numeric(4,0) NOT NULL,
    subcta character varying(10) COLLATE pg_catalog."default",
    asiento integer NOT NULL,
    orden smallint NOT NULL,
    registro integer,
    tipo character varying(1) COLLATE pg_catalog."default",
    base_1 numeric(16,5),
    base_1_base numeric(16,5),
    base_1_euro numeric(16,5),
    cuota_1 numeric(16,5),
    cuota_1_base numeric(16,5),
    cuota_1_euro numeric(16,5),
    tipo_1 numeric(4,2),
    recargo_1 numeric(4,2),
    origen_1 character varying(1) COLLATE pg_catalog."default",
    base_2 numeric(16,5),
    base_2_base numeric(16,5),
    base_2_euro numeric(16,5),
    cuota_2 numeric(16,5),
    cuota_2_base numeric(16,5),
    cuota_2_euro numeric(16,5),
    tipo_2 numeric(4,2),
    recargo_2 numeric(4,2),
    origen_2 character varying(1) COLLATE pg_catalog."default",
    base_3 numeric(16,5),
    base_3_base numeric(16,5),
    base_3_euro numeric(16,5),
    cuota_3 numeric(16,5),
    cuota_3_base numeric(16,5),
    cuota_3_euro numeric(16,5),
    tipo_3 numeric(4,2),
    recargo_3 numeric(4,2),
    origen_3 character varying(1) COLLATE pg_catalog."default",
    moneda character varying(3) COLLATE pg_catalog."default",
    cambio numeric(10,6),
    cambio_euro numeric(10,6),
    fecha_contable date,
    documento character varying(8) COLLATE pg_catalog."default",
    triangulado character varying(1) COLLATE pg_catalog."default"
    SELECT IVA.*,
	IVA.empresa as empresa_id,
	IVA.empresa || '_' || IVA.ejercicio || '_' || IVA.asiento || '_' || IVA.documento as document_id,
	IVA.empresa || '_' || IVA.ejercicio || '_' || IVA.asiento || '_' || IVA.documento as name
	FROM IVA
	WHERE IVA.ejercicio='2023' 
'''


from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

class AurbHdtDocumentTax(models.Model):
    _name = "aurb.hdt.document.tax"
    _description = "AURB document's tax"
    _rec_name = "name"

    name = fields.Char(index=True, required=True)
    
    empresa = fields.Integer()
    ejercicio = fields.Integer()
    subcta = fields.Char()
    asiento = fields.Integer()
    asiento_id = fields.Many2one('aurb.hdt.accounting.entries', string = 'asiento_id')
    total_id = fields.Many2one('aurb.hdt.document.total', string = "total_id")
    orden = fields.Integer()
    registro = fields.Integer()
    tipo = fields.Char() 
    base_1 = fields.Float()
    base_1_base = fields.Float()
    base_1_euro = fields.Float()
    cuota_1 = fields.Float()
    cuota_1_base = fields.Float()
    cuota_1_euro = fields.Float()
    tipo_1 = fields.Float()
    recargo_1 = fields.Float()
    origen_1 = fields.Char()
    base_2 = fields.Float()
    base_2_base = fields.Float()
    base_2_euro = fields.Float()
    cuota_2 = fields.Float()
    cuota_2_base = fields.Float()
    cuota_2_euro = fields.Float()
    tipo_2 = fields.Float()
    recargo_2 = fields.Float()
    origen_2 =fields.Char()
    base_3 = fields.Float()
    base_3_base = fields.Float()
    base_3_euro = fields.Float()
    cuota_3 = fields.Float()
    cuota_3_base = fields.Float()
    cuota_3_euro = fields.Float()
    tipo_3 = fields.Float()
    recargo_3 = fields.Float()
    origen_3 = fields.Char()
    moneda = fields.Char()
    cambio = fields.Float()
    cambio_euro = fields.Float()
    fecha_contable = fields.Date()
    documento = fields.Char() 
    triangulado = fields.Char()
    empresa_id =fields.Many2one('aurb.hdt.company',string ='empresa_id')