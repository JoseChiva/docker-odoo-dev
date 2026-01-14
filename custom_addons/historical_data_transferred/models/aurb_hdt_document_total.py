'''
    empresa smallint NOT NULL,
    ejercicio smallint NOT NULL,
    almacen character varying(2) COLLATE pg_catalog."default" NOT NULL,
    documento integer NOT NULL,
    tipo_doc character varying(2) COLLATE pg_catalog."default" NOT NULL,
    subcta character varying(9) COLLATE pg_catalog."default",
    linea_producto smallint,
    fecha_documento date,
    vendedor_1 character varying(9) COLLATE pg_catalog."default",
    vendedor_2 character varying(9) COLLATE pg_catalog."default",
    vendedor_3 character varying(9) COLLATE pg_catalog."default",
    marca character varying(10) COLLATE pg_catalog."default",
    m_base_bta1 numeric(16,5),
    m_base_bta2 numeric(16,5),
    m_base_bta3 numeric(16,5),
    m_base_bta4 numeric(16,5),
    m_base_bta5 numeric(16,5),
    m_base_bta6 numeric(16,5),
    m_base_bta7 numeric(16,5),
    m_base_bta8 numeric(16,5),
    m_base_nta1 numeric(16,5),
    m_base_nta2 numeric(16,5),
    m_base_nta3 numeric(16,5),
    m_base_nta4 numeric(16,5),
    m_base_nta5 numeric(16,5),
    m_base_nta6 numeric(16,5),
    m_base_nta7 numeric(16,5),
    m_base_nta8 numeric(16,5),
    m_iva_1 numeric(16,5),
    m_iva_2 numeric(16,5),
    m_iva_3 numeric(16,5),
    m_iva_4 numeric(16,5),
    m_iva_5 numeric(16,5),
    m_iva_6 numeric(16,5),
    m_iva_7 numeric(16,5),
    m_iva_8 numeric(16,5),
    m_req_1 numeric(16,5),
    m_req_2 numeric(16,5),
    m_req_3 numeric(16,5),
    m_req_4 numeric(16,5),
    m_req_5 numeric(16,5),
    m_req_6 numeric(16,5),
    m_req_7 numeric(16,5),
    m_req_8 numeric(16,5),
    m_descuento_2 numeric(16,5),
    m_descuento_3 numeric(16,5),
    m_descuento_pp numeric(16,5),
    m_cargo_2 numeric(16,5),
    m_cargo_f numeric(16,5),
    m_irpf numeric(16,5),
    m_total_doc numeric(16,5),
    b_base_bta1 numeric(16,5),
    b_base_bta2 numeric(16,5),
    b_base_bta3 numeric(16,5),
    b_base_bta4 numeric(16,5),
    b_base_bta5 numeric(16,5),
    b_base_bta6 numeric(16,5),
    b_base_bta7 numeric(16,5),
    b_base_bta8 numeric(16,5),
    b_base_nta1 numeric(16,5),
    b_base_nta2 numeric(16,5),
    b_base_nta3 numeric(16,5),
    b_base_nta4 numeric(16,5),
    b_base_nta5 numeric(16,5),
    b_base_nta6 numeric(16,5),
    b_base_nta7 numeric(16,5),
    b_base_nta8 numeric(16,5),
    b_iva_1 numeric(16,5),
    b_iva_2 numeric(16,5),
    b_iva_3 numeric(16,5),
    b_iva_4 numeric(16,5),
    b_iva_5 numeric(16,5),
    b_iva_6 numeric(16,5),
    b_iva_7 numeric(16,5),
    b_iva_8 numeric(16,5),
    b_req_1 numeric(16,5),
    b_req_2 numeric(16,5),
    b_req_3 numeric(16,5),
    b_req_4 numeric(16,5),
    b_req_5 numeric(16,5),
    b_req_6 numeric(16,5),
    b_req_7 numeric(16,5),
    b_req_8 numeric(16,5),
    b_descuento_2 numeric(16,5),
    b_descuento_3 numeric(16,5),
    b_descuento_pp numeric(16,5),
    b_cargo_2 numeric(16,5),
    b_cargo_f numeric(16,5),
    b_irpf numeric(16,5),
    b_total_doc numeric(16,5),
    e_base_bta1 numeric(16,5),
    e_base_bta2 numeric(16,5),
    e_base_bta3 numeric(16,5),
    e_base_bta4 numeric(16,5),
    e_base_bta5 numeric(16,5),
    e_base_bta6 numeric(16,5),
    e_base_bta7 numeric(16,5),
    e_base_bta8 numeric(16,5),
    e_base_nta1 numeric(16,5),
    e_base_nta2 numeric(16,5),
    e_base_nta3 numeric(16,5),
    e_base_nta4 numeric(16,5),
    e_base_nta5 numeric(16,5),
    e_base_nta6 numeric(16,5),
    e_base_nta7 numeric(16,5),
    e_base_nta8 numeric(16,5),
    e_iva_1 numeric(16,5),
    e_iva_2 numeric(16,5),
    e_iva_3 numeric(16,5),
    e_iva_4 numeric(16,5),
    e_iva_5 numeric(16,5),
    e_iva_6 numeric(16,5),
    e_iva_7 numeric(16,5),
    e_iva_8 numeric(16,5),
    e_req_1 numeric(16,5),
    e_req_2 numeric(16,5),
    e_req_3 numeric(16,5),
    e_req_4 numeric(16,5),
    e_req_5 numeric(16,5),
    e_req_6 numeric(16,5),
    e_req_7 numeric(16,5),
    e_req_8 numeric(16,5),
    e_descuento_2 numeric(16,5),
    e_descuento_3 numeric(16,5),
    e_descuento_pp numeric(16,5),
    e_cargo_2 numeric(16,5),
    e_cargo_f numeric(16,5),
    e_irpf numeric(16,5),
    e_total_doc numeric(16,5)

'''
from odoo import models, fields, api, tools
from odoo.exceptions import UserError, ValidationError
from odoo import _

class AurbHdtDocumentTotal(models.Model):
    _name = "aurb.hdt.document.total"
    _description = "AURB document's total"
    _rec_name = "name"

    name = fields.Char(index = True , required = True)
    empresa = fields.Integer()
    ejercicio = fields.Integer()
    almacen = fields.Char()
    documento = fields.Integer()
    tax_ids = fields.One2many('aurb.hdt.document.tax','total_id')
    documento_id = fields.Many2one('aurb.hdt.document', string = 'documento_id')
    empresa_id =fields.Many2one('aurb.hdt.company',string ='empresa_id')

    tipo_doc =fields.Char()
    subcta = fields.Char()
    linea_producto = fields.Char()
    fecha_documento =fields.Date()
    vendedor_1 = fields.Char()
    vendedor_2 = fields.Char()
    vendedor_3 = fields.Char()
    marca = fields.Char()
    m_base_bta1 = fields.Float()
    m_base_bta2 = fields.Float()
    m_base_bta3 = fields.Float()
    m_base_bta4 = fields.Float()
    m_base_bta5 = fields.Float()
    m_base_bta6 = fields.Float()
    m_base_bta7 = fields.Float()
    m_base_bta8 = fields.Float()
    m_base_nta1 = fields.Float()
    m_base_nta2 = fields.Float()
    m_base_nta3 = fields.Float()
    m_base_nta4 = fields.Float()
    m_base_nta5 = fields.Float()
    m_base_nta6 = fields.Float()
    m_base_nta7 = fields.Float()
    m_base_nta8 = fields.Float()
    m_iva_1 = fields.Float()
    m_iva_2 = fields.Float()
    m_iva_3 = fields.Float()
    m_iva_4 = fields.Float()
    m_iva_5 = fields.Float()
    m_iva_6 = fields.Float()
    m_iva_7 = fields.Float()
    m_iva_8 = fields.Float()
    m_req_1 = fields.Float()
    m_req_2 = fields.Float()
    m_req_3 = fields.Float()
    m_req_4 = fields.Float()
    m_req_5 = fields.Float()
    m_req_6 = fields.Float()
    m_req_7 = fields.Float()
    m_req_8 = fields.Float()
    m_descuento_2 = fields.Float() 
    m_descuento_3 = fields.Float()
    m_descuento_pp = fields.Float()
    m_cargo_2 = fields.Float()
    m_cargo_f = fields.Float()
    m_irpf = fields.Float()
    m_total_doc = fields.Float()
    b_base_bta1 = fields.Float()
    b_base_bta2 = fields.Float()
    b_base_bta3 = fields.Float()
    b_base_bta4 = fields.Float()
    b_base_bta5 = fields.Float()
    b_base_bta6 = fields.Float()
    b_base_bta7 = fields.Float()
    b_base_bta8 = fields.Float()
    b_base_nta1 = fields.Float()
    b_base_nta2 = fields.Float()
    b_base_nta3 = fields.Float()
    b_base_nta4 = fields.Float()
    b_base_nta5 = fields.Float()
    b_base_nta6 = fields.Float()
    b_base_nta7 = fields.Float()
    b_base_nta8 = fields.Float()
    b_iva_1 = fields.Float()
    b_iva_2 = fields.Float()
    b_iva_3 = fields.Float()
    b_iva_4 = fields.Float()
    b_iva_5 = fields.Float()
    b_iva_6 = fields.Float()
    b_iva_7 = fields.Float()
    b_iva_8 = fields.Float()
    b_req_1 = fields.Float()
    b_req_2 = fields.Float()
    b_req_3 = fields.Float()
    b_req_4 = fields.Float()
    b_req_5 = fields.Float()
    b_req_6 = fields.Float()
    b_req_7 = fields.Float()
    b_req_8 = fields.Float()
    b_descuento_2 = fields.Float()
    b_descuento_3 = fields.Float()
    b_descuento_pp = fields.Float()
    b_cargo_2 = fields.Float()
    b_cargo_f = fields.Float()
    b_irpf = fields.Float()
    b_total_doc = fields.Float()
    e_base_bta1 = fields.Float()
    e_base_bta2 = fields.Float()
    e_base_bta3 = fields.Float()
    e_base_bta4 = fields.Float()
    e_base_bta5 = fields.Float()
    e_base_bta6 = fields.Float()
    e_base_bta7 = fields.Float()
    e_base_bta8 = fields.Float()
    e_base_nta1 = fields.Float()
    e_base_nta2 = fields.Float()
    e_base_nta3 = fields.Float()
    e_base_nta4 = fields.Float()
    e_base_nta5 = fields.Float()
    e_base_nta6 = fields.Float()
    e_base_nta7 = fields.Float()
    e_base_nta8 = fields.Float()
    e_iva_1 = fields.Float()
    e_iva_2 = fields.Float()
    e_iva_3 = fields.Float()
    e_iva_4 = fields.Float()
    e_iva_5 = fields.Float()
    e_iva_6 = fields.Float()
    e_iva_7 = fields.Float()
    e_iva_8 = fields.Float()
    e_req_1 = fields.Float()
    e_req_2 = fields.Float()
    e_req_3 = fields.Float()
    e_req_4 = fields.Float()
    e_req_5 = fields.Float()
    e_req_6 = fields.Float()
    e_req_7 = fields.Float()
    e_req_8 = fields.Float()
    e_descuento_2 = fields.Float()
    e_descuento_3 = fields.Float()
    e_descuento_pp = fields.Float()
    e_cargo_2 = fields.Float()
    e_cargo_f = fields.Float()
    e_irpf = fields.Float()
    e_total_doc = fields.Float()
    
    ri_base1 = fields.Float(compute = '_compute_tax_ids', default=0)
    ri_cuota1 = fields.Float(default=0)
    ri_tipo1 = fields.Float(default=0)
    ri_recargo1 = fields.Float(default=0)

    ri_base2 = fields.Float(default=0)
    ri_cuota2 = fields.Float(default=0)
    ri_tipo2 = fields.Float(default=0)
    ri_recargo2 = fields.Float(default=0)
    
    ri_base3 = fields.Float(default=0)
    ri_cuota3 = fields.Float(default=0)
    ri_tipo3 = fields.Float(default=0)
    ri_recargo3 = fields.Float(default=0)
    
    
    @api.depends('tax_ids')
    def _compute_tax_ids(self):
        for r in self:
            for i in r.tax_ids:
                r.ri_base1 = i.base_1_base
                r.ri_cuota1 = i.cuota_1_base
                r.ri_tipo1 = i.tipo_1
                r.ri_recargo1 = i.recargo_1

                r.ri_base2 = i.base_2_base
                r.ri_cuota2 = i.cuota_2_base
                r.ri_tipo2 = i.tipo_2
                r.ri_recargo2 = i.recargo_2

                r.ri_base3 = i.base_3_base
                r.ri_cuota3 = i.cuota_3_base
                r.ri_tipo3 = i.tipo_3
                r.ri_recargo3 = i.recargo_3