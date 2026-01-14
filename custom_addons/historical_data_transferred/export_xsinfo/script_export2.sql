
/* 0005 
HDT/Configuration/Countrys/Country	aurb.hdt.country.csv
*/

	copy (
	SELECT *, pais as name,
	'aurb_hdt_country_' || pais as id 
	FROM x0601 
	) to '/tmp/0005aurb.hdt.country.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0010
HDT/Configuration/Empresas	aurb.hdt.company.csv
*/
	copy (
	SELECT *, empresa as name,
	'aurb_hdt_country_' || pais as "pais_id/id",		
	'aurb_hdt_company_'|| empresa as id
	FROM m0101
	union all
	SELECT 0 as empresa,'Sin empresa','','',0,0,0,'','',0,null,'aurb_hdt_company_0'as id
	) to '/tmp/0010aurb.hdt.company.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0020
HDT/Configuration/Warehouse	aurb.hdt.warehouses.csv
*/

	copy (
	SELECT *, empresa as empresa_id, 
	empresa || '_' || almacen as name,
	'aurb_hdt_warehouses_' || empresa || '_' || almacen as id	
	FROM m0401 
	) to '/tmp/0020aurb.hdt.warehouses.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
/* 0030
HDT/Configuration/Currency/Currency	aurb.hdt.currency.csv
*/

	copy (
	SELECT *, 
	moneda as name,
	'aurb_hdt_currency_' || moneda as id 	
	FROM x1301
	) to '/tmp/0030aurb.hdt.currency.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
/* 0040 
HDT/Configuration/Vehicle	aurb.hdt.vehicles.csv
*/

	copy (
	SELECT *, 
	codigo as name,
	'aurb_hdt_vehicles_' || codigo as id 	
	FROM m0601
	) to '/tmp/0040aurb.hdt.vehicles.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
/* 0050 
HDT/Configuration/Exerercises	aurb.hdt.fiscal.year.csv
*/

	copy (
	SELECT empresa, ejercicio, 
	to_char(fecinicio,'MM.DD.YY') as fecinicio,	
	to_char(fecfinal,'MM.DD.YY') as fecfinal,
	estado, 
	coalesce(empresa,0) as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as name,
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as id 
	FROM ejercicios
	) to '/tmp/0050aurb.hdt.fiscal.year.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
/* 0060
HDT/Configuration/Language	aurb.hdt.language.csv
*/

	copy (
	SELECT *, 
	coalesce(idioma, 0) as name,
	'aurb_hdt_language_' ||	coalesce(idioma, 0) as id 
	FROM x2001
	) to '/tmp/0060aurb.hdt.language.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

	
/* 0080
HDT/Configuration/Countrys/Country Ce	aurb.hdt.country.ce.csv
*/
	copy(
	select *, pais as name,
	'aurb_hdt_country_ce_' || pais as id 	
	from x060101
	) to '/tmp/0080aurb.hdt.country.ce.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;	
	
/* 0090
HDT/Configuration/Currency/Currency subaccount	aurb.hdt.currency.subaccount.csv
*/

	copy (
	SELECT *, 
	moneda as moneda_id,
	moneda_ref || '_' || moneda as name,
	'aurb_hdt_currency_subaccount_' ||	moneda_ref || '_' || moneda as id 
	FROM x1302
	) to '/tmp/0090aurb.hdt.currency.subaccount.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0100 
HDT/Configuration/Currency/Currency change	aurb.hdt.currency.change.csv
*/
--(moneda_ref COLLATE pg_catalog."default" ASC NULLS LAST, moneda COLLATE pg_catalog."default" ASC NULLS LAST, fecha_inicio ASC NULLS LAST, tipo ASC NULLS LAST)
	copy (
	SELECT moneda_ref, moneda, 
	to_char(fecha_inicio,'MM.DD.YY') as fecha_inicio,	
	valor_c, valor_v, tipo, 
	moneda as moneda_id,
	moneda_ref || '_' || moneda || '_' || fecha_inicio || '_' || coalesce(tipo,0) as name,
	'aurb_hdt_currency_change_' || moneda_ref || '_' || moneda || '_' || Replace(cast(fecha_inicio as char(10)),'-','_') || '_' || coalesce(tipo,0) as id 	
	FROM x1303
	) to '/tmp/0100aurb.hdt.currency.change.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

	
/* 0110
HDT/Configuration/Accounting/Subaccounts	aurb.hdt.subaccounts.csv
*/

	copy (
	SELECT *, 
	'aurb_hdt_company_'|| empresa as "empresa_id/id", 
	empresa || '_' || coalesce(subcta,'') as name,
	'aurb_hdt_subaccounts_'||empresa || '_' || coalesce(subcta,'') as id		
	FROM subcuentas where empresa in (select empresa from m0101) and trim(coalesce(subcta,'')) !=  ''  order by empresa, subcta 
	) to '/tmp/0110aurb.hdt.subaccounts.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0120
HDT/Configuration/Banks/Bank	aurb.hdt.bank.csv
*/
-- La relación no es correcta debería de depender de subcuenta, el modelo debería tener un subcta_id, pero parecen bancos própios.
	copy (
	SELECT *, 
	empresa as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(subcta, '') as name,
	'aurb_hdt_bank_' || coalesce(empresa,0) || '_' || coalesce(subcta, '') as id 	
	FROM bancos where empresa in (select empresa from m0101) 
	) to '/tmp/0120aurb.hdt.bank.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;



/* 0130
HDT/Configuration/Banks/Bank (more info)	aurb.hdt.bank01.csv  ***Comentar**
*/
 --(subcta COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT *,
	'aurb_hdt_company_'||empresa as "empresa_id/id", 
	'aurb_hdt_bank_'||coalesce(empresa,0) || '_' || coalesce(subcta, '') as "subcta_id/id",
	coalesce(empresa,0) || '_' || coalesce(subcta, '') ||'_' || coalesce(iban,'') as name,
	'aurb_hdt_bank01_'||coalesce(empresa,0) || '_' || coalesce(subcta, '') as id	
	FROM bancos01 where empresa in (select empresa from m0101) 
	) to '/tmp/0130aurb.hdt.bank01.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/* 0140
HDT/Configuration/Banks/Bank entity	aurb.hdt.bank.ent.csv
*/

	copy (
	SELECT *, 
	coalesce(ccc1,'') as name,
	'aurb_hdt_bank_ent_'||coalesce(ccc1,'') as id	
	FROM x1701
	) to '/tmp/0140aurb.hdt.bank.ent.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0150
HDT/Configuration/Banks/Bank office	aurb.hdt.bank.ofi.csv
*/

	copy (
	SELECT *, 
	'aurb_hdt_bank_ent_'||coalesce(ccc1,'') as "ccc1_id/id",
	coalesce(ccc1,'') || '_' || coalesce(ccc2,'') as name,
	'aurb_hdt_bank_ofi_' ||	coalesce(ccc1,'') || '_' || coalesce(ccc2,'') as id
	FROM x170101
	) to '/tmp/0150aurb.hdt.bank.ofi.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0160
HDT/Configuration/Warehouse currency	aurb.hdt.warehouses.currency.csv
*/
	copy (
	SELECT *, 
	'aurb_hdt_company_'||empresa as "empresa_id/id",
	'aurb_hdt_warehouses_'||m0402.empresa || '_' || m0402.almacen as "almacen_id/id",
	'aurb_hdt_currency_'||m0402.moneda_ref as "moneda_ref_id/id",
	'aurb_hdt_currency_'||m0402.moneda_cons as "moneda_cons_id/id",
	m0402.empresa || '_' || m0402.almacen || '_' ||coalesce(m0402.moneda_ref,'NULO') as name,
	'aurb_hdt_warehouses_currency_' || m0402.empresa || '_' || m0402.almacen || '_' ||coalesce(m0402.moneda_ref,'NULO') as id
	FROM m0402 where empresa in (select empresa from m0101)
	) to '/tmp/0160aurb.hdt.warehouses.currency.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 170
HDT/Configuration/Sellers/Seller	aurb.hdt.sellers.csv
*/
--(subcta COLLATE pg_catalog."default" ASC NULLS LAST, linea_producto ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT *, 
	'aurb_hdt_company_'||empresa as "empresa_id/id", 
	coalesce(empresa,0) || '_' || coalesce(subcta,'') as name,
	'aurb_hdt_sellers_' || coalesce(empresa,0) || '_' || coalesce(subcta,'')|| '_' ||coalesce(linea_producto,0) as id	
	FROM m0501 where empresa in (select empresa from m0101)
	) to '/tmp/0170aurb.hdt.sellers.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;	
	
	
	/* 0180
HDT/Configuration/Sellers/Seller commision	aurb.hdt.sellers.commissions.csv
*/
--  (subcta COLLATE pg_catalog."default" ASC NULLS LAST, linea_producto ASC NULLS LAST, codigo COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT *, 
	'aurb_hdt_company_'||empresa as "empresa_id/id", 
	'aurb_hdt_sellers_' || coalesce(empresa,0) || '_' || coalesce(subcta,'')  as "subcta_id/id",
	coalesce(empresa,0) || '_' || coalesce(subcta,'') || '_' ||coalesce(linea_producto,0)||'_' || coalesce(codigo,'') as name,
	'aurb_hdt_sellers_commissions_' || coalesce(empresa,0) || '_' || coalesce(subcta,'') || '_' ||coalesce(linea_producto,0)||'_' || coalesce(codigo,'') as id		
	FROM m050101 where empresa in (select empresa from m0101)
	) to '/tmp/0180aurb.hdt.sellers.commissions.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/* 0190
HDT/Configuration/Sellers/Seller cumulative	aurb.hdt.sellers.accumulated.sales.csv
*/
--  (subcta COLLATE pg_catalog."default" ASC NULLS LAST, linea_producto ASC NULLS LAST, mes ASC NULLS LAST, an ASC NULLS LAST, moneda COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT *, 
	'aurb_hdt_company_'||empresa as "empresa_id/id", 
	'aurb_hdt_sellers_' || coalesce(empresa,0) || '_' || coalesce(subcta,'')  as "subcta_id/id",
	moneda as moneda_id,
	coalesce(subcta,'')||'_'||coalesce(linea_producto,0)||'_'|| coalesce(mes,0)||'_'||coalesce(an,0)||'_'||coalesce(moneda,'')||'_'||coalesce(empresa,0) as name,
	'aurb_hdt_sellers_accumulated_sales_'||coalesce(subcta,'')||'_'||coalesce(linea_producto,0)||'_'|| coalesce(mes,0)||'_'||coalesce(an,0)||'_'||coalesce(moneda,'')||'_'||coalesce(empresa,0) as id
	FROM m0502 where empresa in (select empresa from m0101)
	) to '/tmp/0190aurb.hdt.sellers.accumulated.sales.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0200
HDT/Configuration/Partners/Partner	aurb.hdt.partners.csv
*/
--(subcta COLLATE pg_catalog."default" ASC NULLS LAST, linea_producto ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT m0201.*, 
	'aurb_hdt_company_'||m0201.empresa as "empresa_id/Id",
	'aurb_hdt_subaccounts_'||m0201.empresa || '_' || coalesce(m0201.subcta,'') as "subcta_id/id",
	subcuentas.titulo as name,
	'aurb_hdt_partners_'|| m0201.empresa || '_' || coalesce(m0201.subcta,'')  || '_' || coalesce(m0201.linea_producto,0)  as id	
	FROM m0201 inner join subcuentas on m0201.empresa=subcuentas.empresa and
										m0201.subcta=subcuentas.subcta						
	where m0201.empresa in (select empresa from m0101) --and  empresa || '_' || coalesce(subcta,'') not  in ('1_4310031','1_4310037','1_4310071') 
	) to '/tmp/0200aurb.hdt.partners.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0300
HDT/Configuration/Partners/Partner card	aurb.hdt.partners.card.csv
*/
 --(empresa ASC NULLS LAST, num_tarjeta COLLATE pg_catalog."default" ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST)
	copy (
	SELECT *, 
	'aurb_hdt_company_'||empresa as "empresa_id/Id",
	'aurb_hdt_subaccounts_'||empresa || '_' || coalesce(subcta,'') as "subcta_id/Id",
	empresa || '_' || coalesce(tipo_doc,'x') || '_' || coalesce(num_tarjeta,'') as name,
	'aurb_hdt_partners_card_'||empresa || '_' || coalesce(tipo_doc,'x') || '_' || coalesce(num_tarjeta,'') as id
	FROM m020102 where empresa in (select empresa from m0101)
	) to '/tmp/0300aurb.hdt.partners.card.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
/* 0400
HDT/Configuration/Partners/Partner risk	aurb.hdt.partners.risk.csv
*/
--   (subcta COLLATE pg_catalog."default" ASC NULLS LAST, linea_producto ASC NULLS LAST, moneda COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST)
--		SELECT TO_CHAR(fecha, 'MM.DD.YY') AS fecha_formateada


	copy (
	SELECT m0202.empresa,m0202.subcta,m0202.linea_producto,m0202.clv_sub,m0202.moneda,m0202.limite_credito,m0202.riesgo_cartera,m0202.riesgo_pedidos,
	to_char(m0202.fecha_u_compra,'YYYY-MM-DD') as fecha_u_compra,	
	m0202.pts_no_factura, 
	'aurb_hdt_company_'||m0202.empresa as "empresa_id/Id",
	'aurb_hdt_currency_' || m0202.moneda as "moneda_id/Id", 
	'aurb_hdt_partners_'|| m0202.empresa || '_' || coalesce(m0202.subcta,'') || '_' || coalesce(m0202.linea_producto,0) as "subcta_id/id",
	m0202.empresa || '_' || coalesce(m0202.subcta,'') || '_' || coalesce(m0202.moneda,'')  as name,
	'aurb_hdt_partners_risk_' || m0202.empresa || '_' || coalesce(m0202.subcta,'') || '_' || coalesce(m0202.moneda,'') ||'_'|| coalesce(m0202.linea_producto,0) as id
	FROM m0202 inner join m0201 on m0202.empresa=m0201.empresa and m0202.subcta=m0201.subcta and m0202.linea_producto=m0201.linea_producto
	where m0202.empresa  in (select empresa from m0101) 
	and  'aurb_hdt_partners_'|| m0202.empresa || '_' || coalesce(m0202.subcta,'') || '_' || coalesce(m0202.linea_producto,0)
	not  in ('aurb_hdt_partners_1_4310031_1','aurb_hdt_partners_1_4310037_1','1_4301884','aurb_hdt_partners_19_4400001_1') and m0202.moneda<>'0'
	) to '/tmp/0400aurb.hdt.partners.risk.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/* 0410
HDT/Configuration/Partners/Partner payment terms	aurb.hdt.partners.pay.terms.csv
*/
--(subcta COLLATE pg_catalog."default" ASC NULLS LAST, linea_producto ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT m0204.*, 
	'aurb_hdt_company_'|| m0204.empresa as "empresa_id/Id",
	'aurb_hdt_partners_'|| m0204.empresa || '_' || coalesce(m0204.subcta,'') || '_' || coalesce(m0204.linea_producto,0) as "subcta_id/id",
	m0204.empresa || '_' || coalesce(m0204.subcta,'')||'_'|| coalesce(m0204.linea_producto,0) as name,
	'hdt_partners_pay_terms_' || m0204.empresa || '_' || coalesce(m0204.subcta,'')  || '_' || coalesce(m0204.linea_producto,0)  as id		
	FROM m0204 inner join m0201 on m0204.empresa=m0201.empresa and m0204.subcta=m0201.subcta and m0204.linea_producto=m0201.linea_producto
	where m0204.empresa in (select empresa from m0101) 
	and  'aurb_hdt_partners_'|| m0204.empresa || '_' || coalesce(m0204.subcta,'') || '_' || coalesce(m0204.linea_producto,0)
	not  in ('aurb_hdt_partners_1_4310031_1','aurb_hdt_partners_1_4310037_1','1_4301884','aurb_hdt_partners_19_4400001_1', 'aurb_hdt_partners_1_4310071_1' ) 
	) to '/tmp/0410aurb.hdt.partners.pay.terms.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0420
HDT/Configuration/Partners/Partner account	aurb.hdt.partners.account.csv
*/
-- (subcta COLLATE pg_catalog."default" ASC NULLS LAST, linea_producto ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT m0206.*, 
	'aurb_hdt_company_'|| m0206.empresa as "empresa_id/Id", 
	'aurb_hdt_partners_'|| m0206.empresa || '_' || coalesce(m0206.subcta,'') || '_' || coalesce(m0206.linea_producto,0) as "subcta_id/id",
	 m0206.empresa || '_' || coalesce(m0206.subcta,'')|| coalesce(m0206.linea_producto,0) as name,
	'aurb_hdt_partners_account_' || m0206.empresa || '_' || coalesce(m0206.subcta,'')||'_' || coalesce(m0206.linea_producto,0) as id	
	FROM m0206 inner join m0201 on m0206.empresa=m0201.empresa and m0206.subcta=m0201.subcta and m0206.linea_producto=m0201.linea_producto
	where m0206.empresa in (select empresa from m0101) 
	and  'aurb_hdt_partners_'|| m0206.empresa || '_' || coalesce(m0206.subcta,'') || '_' || coalesce(m0206.linea_producto,0)
	not  in ('aurb_hdt_partners_1_4310031_1','aurb_hdt_partners_1_4310037_1','1_4301884','aurb_hdt_partners_19_4400001_1', 'aurb_hdt_partners_1_4310071_1' ) 
	) to '/tmp/0420aurb.hdt.partners.account.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/*0430
HDT/Configuration/Partners/Partner contact	aurb.hdt.partners.contact.csv
*/
--   (subcta COLLATE pg_catalog."default" ASC NULLS LAST, contacto COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT m0208.*, 
	'aurb_hdt_company_'||m0208.empresa as "empresa_id/Id", 
	'aurb_hdt_partners_'|| m0208.empresa || '_' || coalesce(m0208.subcta,'') || '_' || coalesce(m0201.linea_producto,0) as "subcta_id/id",
	m0208.empresa || '_' || coalesce(m0208.subcta,'') || '_' || coalesce(m0208.contacto,'') as name,
	'aurb_hdt_partners_contact_'||m0208.empresa || '_' || coalesce(m0208.subcta,'') || '_' || replace(replace(coalesce(m0208.contacto,''),'.','_'),' ','R') ||'_' || coalesce(m0201.linea_producto,0) as id
	FROM m0208 inner join m0201 on m0208.empresa=m0201.empresa and m0208.subcta=m0201.subcta 
	where m0208.empresa in (select empresa from m0101) 
	and  'aurb_hdt_partners_'|| m0208.empresa || '_' || coalesce(m0208.subcta,'') || '_' || coalesce(m0201.linea_producto,0)
	not  in ('aurb_hdt_partners_1_4310031_1','aurb_hdt_partners_1_4310037_1','1_4301884','aurb_hdt_partners_19_4400001_1', 'aurb_hdt_partners_1_4310071_1' ) 
	) to '/tmp/0430aurb.hdt.partners.contact.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/*0440
HDT/Configuration/Partners/Partner comments	aurb.hdt.partners.comments.csv
*/
--(subcta COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST, tipo_obs ASC NULLS LAST, numero_obs ASC NULLS LAST)
	copy (
	SELECT m0209.*, 
	'aurb_hdt_company_'||m0209.empresa as "empresa_id/Id", 
	'aurb_hdt_partners_'|| m0209.empresa || '_' || coalesce(m0209.subcta,'') || '_' || coalesce(m0201.linea_producto,0)  as "subcta_id/id",
	m0209.empresa || '_' || coalesce(m0209.subcta,'') || '_' || coalesce(m0209.tipo_obs,0) || '_' || coalesce(numero_obs,0) as name,
	'aurb_hdt_partners_comments_'||m0209.empresa || '_' || coalesce(m0209.subcta,'') || '_' || coalesce(m0209.tipo_obs,0) || '_' || coalesce(m0209.numero_obs,0) ||'_' || coalesce(m0201.linea_producto,0) as id	
	FROM m0209 inner join m0201 on m0209.empresa=m0201.empresa and m0209.subcta=m0201.subcta 
	where m0209.empresa in (select empresa from m0101)
	and  'aurb_hdt_partners_'|| m0209.empresa || '_' || coalesce(m0209.subcta,'') || '_' || coalesce(m0201.linea_producto,0)
	not  in ('aurb_hdt_partners_1_4310031_1','aurb_hdt_partners_1_4310037_1','1_4301884','aurb_hdt_partners_19_4400001_1', 'aurb_hdt_partners_1_4310071_1' ) 
	) to '/tmp/0440aurb.hdt.partners.comments.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
	
/* 0450
HDT/Configuration/Partners/Partner address	aurb.hdt.partners.address.csv
*/
--(subcta COLLATE pg_catalog."default" ASC NULLS LAST, orden ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT direcciones.*, 
	'aurb_hdt_company_'||direcciones.empresa as "empresa_id/Id", 
	'aurb_hdt_partners_'|| direcciones.empresa || '_' || coalesce(direcciones.subcta,'') || '_' || coalesce(m0201.linea_producto,0) as "subcta_id/id",
	direcciones.empresa || '_' || coalesce(direcciones.subcta,'') || '_' || coalesce(direcciones.orden,0) as name,
	'aurb_hdt_partners_address_' || direcciones.empresa || '_' || coalesce(direcciones.subcta,'') || '_' || coalesce(direcciones.orden,0)||'-'||coalesce(m0201.linea_producto,0) as id
	FROM direcciones inner join m0201 on direcciones.empresa=m0201.empresa and direcciones.subcta=m0201.subcta
	where direcciones.empresa in (select empresa from m0101) 
	and  'aurb_hdt_partners_'|| direcciones.empresa || '_' || coalesce(direcciones.subcta,'') || '_' || coalesce(m0201.linea_producto,0)
	not  in ('aurb_hdt_partners_1_4310031_1','aurb_hdt_partners_1_4310037_1','1_4301884','aurb_hdt_partners_19_4400001_1', 'aurb_hdt_partners_1_4310071_1' ) 
	) to '/tmp/0450aurb.hdt.partners.address.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0460
HDT/Items/Item	aurb.hdt.items.csv
*/
--(codigo COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST)
	copy (
	SELECT empresa, codigo, clv_art, codigo_a, tipo, tipo_art, 
	ficha_cerrada, 
	to_char(fecha_baja,'MM.DD.YY') as fecha_baja,
	'aurb_hdt_company_'||empresa as "empresa_id/Id",
	empresa || '_' || codigo as name,
	'aurb_hdt_items_'||empresa || '_' || replace(codigo,' ','E') as id
	FROM m0301 where empresa in (select empresa from m0101) and 'aurb_hdt_items_'||empresa || '_' || replace(codigo,' ','E')='aurb_hdt_items_1_04/1609100050I'
	
	) to '/tmp/0460aurb.hdt.items.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0470
HDT/Items/Item desc	aurb.hdt.items.description.csv
*/

	copy (
	SELECT m0302.*, 
	'aurb_hdt_company_'||m0302.empresa as "empresa_id/Id",
	'aurb_hdt_items_'||m0302.empresa || '_' || replace(m0302.codigo,' ','E') as "codigo_id/id",	
	m0302.empresa || '_' || m0302.codigo || '_' || coalesce(m0302.subcta,'0')|| '_' || coalesce(m0302.idioma,'0') as name,
	'aurb_hdt_items_description_' || m0302.empresa || '_' || replace(m0302.codigo,' ','E') || '_' || coalesce(m0302.subcta,'0')|| '_' || coalesce(m0302.idioma,'0') as id
	FROM m0302 inner join m0301 on m0302.empresa=m0301.empresa and  m0302.codigo=m0301.codigo
	where m0302.empresa in (select empresa from m0101) and 'aurb_hdt_items_'||m0302.empresa || '_' || replace(m0302.codigo,' ','E')='aurb_hdt_items_1_04/1609100050I'
	) to '/tmp/0470aurb.hdt.items.description.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
 


/* 0480
HDT/Items/Item Price	aurb.hdt.items.price.csv
*/
/*  (codigo COLLATE pg_catalog."default" ASC NULLS LAST, empresa ASC NULLS LAST) */

	copy (
	SELECT *, 
	'aurb_hdt_company_'||m0303.empresa as "empresa_id/Id",
	'aurb_hdt_items_'||m0303.empresa || '_' || replace(m0303.codigo,' ','E') as "codigo_id/id",	
	'aurb_hdt_currency_' || m0303.moneda as "moneda_id/id", 
	coalesce(m0303.empresa, 0) || '_' || m0303.codigo as name,
	'aurb_hdt_items_price_'|| coalesce(m0303.empresa, 0) || '_' || replace(m0303.codigo,' ','E') as id
	FROM m0303 inner join m0301 on m0303.empresa=m0301.empresa and  m0303.codigo=m0301.codigo
	where m0303.empresa in( select empresa from m0101)
	) to '/tmp/0480aurb.hdt.items.price.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
/* 0490
HDT/Items/Item batch	aurb.hdt.items.batch.csv
*/
-- (empresa ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, lote_interno COLLATE pg_catalog."default" ASC NULLS LAST)
	copy (
	SELECT m0319.empresa, m0319.codigo, m0319.lote_interno, m0319.lote_compra, m0319.almacen, m0319.ubicacion, m0319.stock_actual, m0319.stock_bultos, 
	m0319.stock_reserva, m0319.stock_reserva_b, 
	to_char(m0319.fecha_cad,'MM.DD.YY') as fecha_cad,
	m0319.estado, 
	to_char(m0319.fecha_alta,'MM.DD.YY') as fecha_alta,	
	to_char(m0319.fecha_bloq,'MM.DD.YY') as fecha_bloq,
	m0319.motivo, m0319.observacion, m0319.codigo_prov, m0319.cantidad_entra, m0319.subcta_prov, m0319.cod_mezcla, m0319.rendimiento, m0319.precio, m0319.cantidad_real, m0319.ejercicio, 
	m0319.documento, m0319.tipo_doc, m0319.linea_doc, m0319.orden, m0319.campo1, m0319.campo2, m0319.campo3, m0319.campo4, m0319.campo5, 
	m0319.cantidad_bruta, m0319.presentacion, m0319.urdido, m0319.pieza_teje, m0319.documento_teje, 
	m0319.stock_reserva_cp, m0319.stock_reserva_bcp, 
	'aurb_hdt_company_'||m0319.empresa as "empresa_id/Id",
	'aurb_hdt_items_'||m0319.empresa || '_' || replace(m0319.codigo,' ','E') as "codigo_id/id",	
	'aurb_hdt_warehouses_' || m0319.empresa || '_' || m0319.almacen as "almacen_id/id",
	m0319.empresa || '_' || m0319.almacen || '_' || m0319.codigo || '_' || m0319.lote_interno as name,
	'aurb_hdt_items_batch_' || m0319.empresa || '_' || m0319.almacen || '_' || m0319.codigo || '_' || m0319.lote_interno as id	
	FROM m0319 inner join m0301 on m0319.empresa=m0301.empresa and  m0319.codigo=m0301.codigo 
	where m0319.empresa in ( select empresa from m0101)
	) to '/tmp/0490aurb.hdt.items.batch.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0500 Repasar no tiene registros
HDT/Items/Items batch piece	aurb.hdt.items.batch.piece.csv
*/
-- (npieza COLLATE pg_catalog."default" ASC NULLS LAST)
	copy (
	SELECT empresa, almacen, codigo, npieza, lote_interno, ubicacion, calidad, anchura, cantidad, cantidad_s, tara_desc, tara_m, 
	to_char(fecha_fabrica,'MM.DD.YY') as fecha_fabrica,	
	hora_fabrica, repasador, tabla_repaso, bonificacion, motivo_boni, coste_m, 
	empresa as empresa_id, 
	empresa || '_' || almacen as almacen_id,
	empresa || '_' || almacen || '_' || codigo as codigo_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno as lote_interno_id,
	npieza as name,
	'aurb_hdt_items_batch_piece_' || npieza as id	
	FROM m031901 where empresa in ( select empresa from m0101)
	) to '/tmp/0500aurb.hdt.items.batch.piece.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0510 No tiene registros Repasar 
HDT/Items/Item batch incident	aurb.hdt.items.batch.incident.csv
*/
--No tiene índice igual no se utiliza (repasar)
	copy (
	SELECT empresa, almacen, codigo, lote_interno, lote_compra, incidencia, 
	to_char(fecha_entrada,'MM.DD.YY') as fecha_entrada,
	hora_entrada, usuario_entrada, 
	empresa as empresa_id, 
	empresa || '_' || almacen as almacen_id,
	empresa || '_' || almacen || '_' || codigo as codigo_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno as lote_interno_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno || '_' || incidencia as name,
	'aurb_hdt_items_batch_incident_' || empresa || '_' || almacen || '_' || codigo || '_' || lote_interno || '_' || incidencia as id	
	FROM m031903 where empresa in ( select empresa from m0101)
	) to '/tmp/0510aurb.hdt.items.batch.incident.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0520
HDT/Sales/ Sales Order/Sales Order Head	aurb.hdt.order.header.csv
*/
--(empresa ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST, documento ASC NULLS LAST) versión SE
-- (empresa ASC NULLS LAST, ejercicio ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST, documento ASC NULLS LAST)
--Añado ejercicios para versiones no se
	copy ( 
	SELECT v0101.empresa, ejercicio, subcta, clv_sub, orden, almacen, clv_ped, documento, 
	to_char(fecha_documento,'MM.DD.YY') as fecha_documento, 
	tipo_doc, referencia, tipo_forma_pago, numero_recibos, primer_intervalo, otros_intervalos, dia_fijo_pago_1, dia_fijo_pago_2,
	descuento_p_pago, descuento_2, descuento_3, tarifa, categoria, tipo_iva, cargo_financiero, cargo_fin_dias, cargo_2, irpf, aplic_irpf, portes, 
	agencia_transporte, pedido_definitivo, albaran_factura, alternativo, subcta_facturacion, subcta_contable, linea_producto, 
	intervalo_factura, vendedor_1, vendedor_2, vendedor_3, clv_ven_1, clv_ven_2, clv_ven_3, ctd_cuenta, ctd_cuenta_base, ctd_cuenta_euro,
	moneda, cambio, cambio_euro, situacion, recepcion, 
	to_char(fecha_valor,'MM.DD.YY') as fecha_valor,
	to_char(fecha_entrada,'MM.DD.YY') as fecha_entrada,
	usuario_entrada, hora_entrada, 
	to_char(fecha_modifi,'MM.DD.YY') as fecha_modifi, 
	usuario_modifi, hora_modifi, origen_oferta, triangulado, ccc1, ccc2, dc, numero_cuenta, codexpe, campo1, campo2, swift, iban,
	'aurb_hdt_company_'||v0101.empresa as "empresa_id/Id",
	'aurb_hdt_currency_' || v0101.moneda as "moneda_id/id", 	
	'aurb_hdt_warehouses_' || v0101.empresa || '_' || v0101.almacen as "almacen_id/id", 
    'aurb_hdt_partners_'|| v0101.empresa || '_' || coalesce(v0101.subcta,'')  || '_' || coalesce(v0101.linea_producto,0) as "ic_id/id",		
	--'aurb_hdt_document_' || v0101.empresa || '_' || v0101.ejercicio || '_' || v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento  as "documento_id/id",
	v0101.empresa || '_' || v0101.ejercicio || '_' || v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento as name, 
	'aurb_hdt_order_header_' || v0101.empresa || '_' || v0101.ejercicio || '_' || v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento as id
	FROM v0101
	WHERE Ejercicio='2024' and empresa in ( select empresa from m0101)
	 ) to '/tmp/0520aurb.hdt.order.header.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/*0530
HDT/Sales/ Sales Order/Sales Order Lines	aurb.hdt.order.lines.csv
*/
--(empresa ASC NULLS LAST, ejercicio ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, tipo_movimiento COLLATE pg_catalog."default" ASC NULLS LAST, pedido ASC NULLS LAST, linea_pedido ASC NULLS LAST) no SE
	copy ( 
	SELECT v010101.empresa, v010101.ejercicio, tipo_movimiento, pedido, linea_pedido, v010101.clv_ped, 
	to_char(fecha_servicio,'MM.DD.YY') as fecha_servicio,
	articulo, acumula, cantidad, bultos, cantidad_s, bultos_s, precio, precio_iva, tipo_precio, v010101.descuento_1, v010101.descuento_2, v010101.descuento_3, 
	comision_1, comision_2, comision_3, v010101.tipo_iva, variante, iva, recargo_e, precio_coste, pts_kl, aplic_pt_kl, total_linea, total_linea_base, total_linea_euro, 
	v010101.moneda, v010101.cambio, v010101.cambio_euro, v010101.almacen, v010101.subcta, v010101.linea_producto, v010101.clv_sub, 
	to_char(v010101.fecha_documento,'MM.DD.YY') as fecha_documento,
	presupuesto, linea_presupuesto, v010101.triangulado, lote_interno, od_linea, v010101.codexpe, v010101.campo1, v010101.campo2, v010101.porcentaje, v010101.eur_kg,
	'aurb_hdt_company_'||v010101.empresa as "empresa_id/Id",
	'aurb_hdt_currency_' || v010101.moneda as "moneda_id/id", 
	'aurb_hdt_warehouses_' || v010101.empresa || '_' || v010101.almacen as "almacen_id/id",  
	case when left(Ltrim(articulo)='..',2) then null
	else
	'aurb_hdt_items_'||v010101.empresa || '_' || replace(v010101.articulo,' ','E') 
	end as "articulo_id/id", 
	'aurb_hdt_order_header_'||v0101.empresa || '_' || v0101.ejercicio ||'_'|| v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento as "pedido_id/id",
	v0101.empresa || '_' || v0101.ejercicio ||'_'|| v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento || '_' || v010101.linea_pedido as name,
	'aurb_hdt_order_lines_'||v0101.empresa || '_' || v0101.ejercicio ||'_'|| v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento || '_' || v010101.linea_pedido as id		
	FROM v0101
	JOIN v010101 ON v0101.empresa=v010101.empresa and v0101.ejercicio=v010101.ejercicio and 
	v0101.tipo_doc=v010101.tipo_movimiento and 
	v0101.documento=v010101.pedido and
	v0101.almacen=v010101.almacen
	WHERE v0101.ejercicio='2024' and v010101.empresa in ( select empresa from m0101) 
	 ) to '/tmp/0530aurb.hdt.order.lines.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;		


/* 0535
HDT/Sales/ Sales Order/Sales Order Manual Description	aurb.hdt.order.man.description.csv
*/
	copy ( 
	SELECT vxxxx01.*,
	'aurb_hdt_company_'||vxxxx01.empresa as "empresa_id/id",
	'aurb_hdt_warehouses_'||vxxxx01.empresa || '_' || vxxxx01.almacen as "almacen_id/id", 
	vxxxx01.empresa || '_' || vxxxx01.ejercicio ||'_' || vxxxx01.almacen || '_' ||  vxxxx01.tipo_doc || '_' || vxxxx01.documento || '_' || vxxxx01.orden as name,
	'aurb_hdt_order_lines_'|| vxxxx01.empresa || '_' || vxxxx01.ejercicio ||'_' || vxxxx01.almacen || '_' || vxxxx01.tipo_doc || '_' ||   vxxxx01.documento || '_' || vxxxx01.orden ||'_aurb_hdt_document_lines' as  "documento_id/id",
	'aurb_hdt_order_man_description_' || vxxxx01.empresa || '_' || vxxxx01.ejercicio ||'_' || vxxxx01.almacen || '_' ||  vxxxx01.tipo_doc ||'_'|| vxxxx01.documento || '_' || vxxxx01.orden as id	
	FROM vxxxx01  INNER JOIN V010101 ON vxxxx01.empresa=v010101.empresa 
	and vxxxx01.ejercicio=v010101.ejercicio 
	and vxxxx01.almacen=v010101.almacen
	and vxxxx01.tipo_doc=v010101.tipo_movimiento
	and vxxxx01.documento=v010101.pedido
	and vxxxx01.orden=v010101.linea_pedido
	WHERE vxxxx01.ejercicio='2024' and vxxxx01.empresa in ( select empresa from m0101) 
	 ) to '/tmp/0535aurb.hdt.document.lines.manual.desc.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0540
aurb.hdt.document.total.csv
*/
-- (empresa ASC NULLS LAST, ejercicio ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, documento ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST)
--aurb_hdt_order_header_1_2023_1_PC_23000013_aurb_hdt_document
copy ( 
SELECT vxx03.*,
vxx03.empresa as empresa_id,
'aurb_hdt_order_header_'||vxx03.empresa || '_' || vxx03.ejercicio ||'_' || vxx03.almacen || '_' || vxx03.tipo_doc || '_' || vxx03.documento ||'_aurb_hdt_document' as "document_id/id",
vxx03.empresa || '_' || vxx03.ejercicio ||'_' || vxx03.almacen || '_' || vxx03.tipo_doc || '_' || vxx03.documento as name,
'aurb_hdt_document_total_'||vxx03.empresa || '_' || vxx03.ejercicio ||'_' || vxx03.almacen || '_' || vxx03.tipo_doc || '_' || vxx03.documento as id
FROM vxx03 inner join v0101 on vxx03.empresa= v0101.empresa 
and vxx03.ejercicio=v0101.ejercicio
and vxx03.almacen = v0101.almacen
and vxx03.tipo_doc = v0101.tipo_doc
and vxx03.documento = v0101.documento
WHERE vxx03.ejercicio='2024' and vxx03.empresa in (select empresa from m0101) 
	 ) to '/tmp/0540aurb.hdt.document.total_pedidos.csv'  header csv delimiter ';'; 

/*0550
HDT/Sales/Delivery/Sales Delivery Head	aurb.hdt.delivery.header.csv
*/
--(empresa ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST, subcta COLLATE pg_catalog."default" ASC NULLS LAST)
copy ( 
SELECT V0201.*,
'aurb_hdt_company_'||v0201.empresa as "empresa_id/Id",
'aurb_hdt_currency_' || v0201.moneda as "moneda_id/id", 	
'aurb_hdt_warehouses_' || v0201.empresa || '_' || v0201.almacen as "almacen_id/id", 
'aurb_hdt_partners_'|| v0201.empresa || '_' || coalesce(v0201.subcta,'')  || '_' || coalesce(v0201.linea_producto,0) as "ic_id/id",		
V0201.empresa || '_' || V0201.ejercicio || '_' || V0201.almacen || '_' || V0201.tipo_doc || '_' || V0201.documento as name, 
'aurb_hdt_delivery_header_'||V0201.empresa || '_' || V0201.ejercicio || '_' || V0201.almacen || '_' || V0201.tipo_doc || '_' || V0201.documento as id	
FROM V0201
JOIN M0101 ON V0201.empresa=M0101.empresa 
WHERE Ejercicio='2023'
 ) to '/tmp/0550aurb.hdt.delivery.header.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0555
aurb.hdt.invoice
*/
copy ( 
SELECT v0301.*,
'aurb_hdt_company_'||v0301.empresa as "empresa_id/Id",
'aurb_hdt_currency_' || v0301.moneda as "moneda_id/id", 	
'aurb_hdt_warehouses_' || v0301.empresa || '_' || v0301.almacen as "almacen_id/id", 
'aurb_hdt_partners_'|| v0301.empresa || '_' || coalesce(v0301.subcta,'')  || '_' || coalesce(v0301.linea_producto,0) as "ic_id/id",		
V0301.empresa || '_' || V0301.ejercicio || '_' || V0301.almacen || '_' || V0301.tipo_doc || '_' || V0301.documento as name,
'aurb_hdt_invoice_header_'||V0301.empresa || '_' || V0301.ejercicio || '_' || V0301.almacen || '_' || V0301.tipo_doc || '_' || V0301.documento as id
FROM V0301
JOIN M0101 ON V0301.empresa=M0101.empresa 
WHERE Ejercicio='2023'
 ) to '/tmp/0555aurb.hdt.invoice.header.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;




/*0555
HDT/Sales/Delivery/Sales Delivery Lines	aurb.hdt.delivery.lines.csv f
*/
-- (empresa ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, tipo_movimiento COLLATE pg_catalog."default" ASC NULLS LAST, albaran ASC NULLS LAST, linea_albaran ASC NULLS LAST)
copy ( 
SELECT v020101.*,
'aurb_hdt_company_'||v0201.empresa as "empresa_id/Id",		
'aurb_hdt_warehouses_' || v0201.empresa || '_' || v0201.almacen as "almacen_id/id", 
case when left(Ltrim(v020101.articulo),2)='..' then null
else
	'aurb_hdt_items_'||v020101.empresa || '_' || replace(v020101.articulo,' ','E') 
end as "articulo_id/id", 
'aurb_hdt_delivery_header_'||v0201.empresa || '_' || v0201.ejercicio ||'_'|| v0201.almacen || '_' || v0201.tipo_doc || '_' || v0201.documento as "albaran_id/id",
'aurb_hdt_invoice_header_'||v0201.empresa || '_' || v0201.ejercicio ||'_'|| v0201.almacen || '_' || CASE v0201.tipo_doc WHEN 'EC' THEN 'FC' WHEN 'SV' THEN 'FV' END || '_' || v0201.factura as "factura_id/id",
v0201.empresa || '_' || v0201.ejercicio ||'_'|| v0201.almacen || '_' || v0201.tipo_doc || '_' || v0201.documento || '_' || v020101.linea_albaran as name,
'aurb_hdt_delivery_lines_'||v0201.empresa || '_' || v0201.ejercicio ||'_'|| v0201.almacen || '_' || v0201.tipo_doc || '_' || v0201.documento || '_' || v020101.linea_albaran as id		
FROM v0201
JOIN v020101 ON v0201.empresa=v020101.empresa and v0201.ejercicio=v020101.ejercicio and 
v0201.tipo_doc=v020101.tipo_movimiento and 
v0201.documento=v020101.albaran and
v0201.almacen=v020101.almacen
WHERE v0201.ejercicio='2023' and v0201.empresa in (select empresa from m0101) 
) to '/tmp/0555aurb.hdt.delivery.lines.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
 
/*0560
HDT/Sales/Delivery/Sales Delivery Lines	aurb.hdt.invoice.lines.csv facturas lieas
*/ 
 
copy ( 
SELECT 
'aurb_hdt_invoice_header_'||v0201.empresa || '_' || v0201.ejercicio ||'_'|| v0201.almacen || '_' || CASE v020101.tipo_movimiento WHEN 'EC' THEN 'FC' WHEN 'SV' THEN 'FV' END || '_' || v0201.factura as "factura_id/id",
'aurb_hdt_delivery_lines_'||v0201.empresa || '_' || v0201.ejercicio ||'_'|| v0201.almacen || '_' || v0201.tipo_doc || '_' || v0201.documento || '_' || v020101.linea_albaran as id		
FROM v0201
inner JOIN v020101 ON v0201.empresa=v020101.empresa and v0201.ejercicio=v020101.ejercicio and 
v0201.tipo_doc=v020101.tipo_movimiento and 
v0201.documento=v020101.albaran and 
v0201.almacen=v020101.almacen 
inner join v0301 on
v0301.empresa=v020101.empresa and v0301.ejercicio=v020101.ejercicio and 
v0301.tipo_doc=CASE v020101.tipo_movimiento WHEN 'EC' THEN 'FC' WHEN 'SV' THEN 'FV' END  and 
v0301.documento=v020101.albaran and
v0301.almacen=v020101.almacen 	
WHERE v0201.ejercicio='2023' and v0201.empresa in (select empresa from m0101)
 ) to '/tmp/0560aurb.hdt.invoice.lines.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
 
/* 0570
HDT/Sales/ Sales Order/Sales Order Manual Description albaranes aurb.hdt.order.man.delibery.description.csv
*/
	copy ( 
	SELECT vxxxx01.*,
	'aurb_hdt_company_'||vxxxx01.empresa as "empresa_id/id",
	'aurb_hdt_warehouses_'||vxxxx01.empresa || '_' || vxxxx01.almacen as "almacen_id/id", 
	vxxxx01.empresa || '_' || vxxxx01.ejercicio ||'_' || vxxxx01.almacen || '_' ||  vxxxx01.tipo_doc || '_' || vxxxx01.documento || '_' || vxxxx01.orden as name,
	'aurb_hdt_delivery_lines_'|| vxxxx01.empresa || '_' || vxxxx01.ejercicio ||'_' || vxxxx01.almacen || '_' || vxxxx01.tipo_doc || '_' ||   vxxxx01.documento || '_' || vxxxx01.orden ||'_aurb_hdt_document_lines' as  "documento_id/id",
	'aurb_hdt_delivery_man_description_' || vxxxx01.empresa || '_' || vxxxx01.ejercicio ||'_' || vxxxx01.almacen || '_' ||  vxxxx01.tipo_doc ||'_'|| vxxxx01.documento || '_' || vxxxx01.orden as id	
	FROM vxxxx01  INNER JOIN V020101 ON vxxxx01.empresa=v020101.empresa 
	and vxxxx01.ejercicio=v020101.ejercicio 
	and vxxxx01.almacen=v020101.almacen
	and vxxxx01.tipo_doc=v020101.tipo_movimiento
	and vxxxx01.documento=v020101.albaran
	and vxxxx01.orden=v020101.linea_albaran
	WHERE vxxxx01.ejercicio='2023' and vxxxx01.empresa in ( select empresa from m0101) 
	 ) to '/tmp/0570aurb.hdt.document.deliverylines.manual.desc.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

--aurb_hdt_delivery_lines_1_2023_1_EC_23000002_6_aurb_hdt_document_lines

/* 0590 Facturas total
aurb.hdt.document.totalalbaranes.csv
*/
-- (empresa ASC NULLS LAST, ejercicio ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, documento ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST)
--aurb_hdt_order_header_1_2023_1_PC_23000013_aurb_hdt_document
copy ( 
SELECT vxx04.*, 
'aurb_hdt_company_'||vxx04.empresa as "empresa_id/id",
'aurb_hdt_invoice_header_'||vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento ||'_aurb_hdt_document' as "documento_id/id",
vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as name,
'aurb_hdt_document_total_'||vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as id
FROM vxx04 inner join v0301 on vxx04.empresa= v0301.empresa 
and vxx04.ejercicio=v0301.ejercicio
and vxx04.almacen = v0301.almacen
and vxx04.tipo_doc = v0301.tipo_doc
and vxx04.documento = v0301.documento
WHERE vxx04.ejercicio='2023' and vxx04.empresa in (select empresa from m0101) 
	 ) to '/tmp/0590aurb.hdt.document.total_Facturas.csv'  header csv delimiter ';'; 

select * from iva limit 100
/* 0590 Facturas total
aurb.hdt.document.totalalbaranes.csv
*/
-- (empresa ASC NULLS LAST, ejercicio ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, documento ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST)
--aurb_hdt_order_header_1_2023_1_PC_23000013_aurb_hdt_document
copy ( 
SELECT vxx04.*, 
'aurb_hdt_company_'||vxx04.empresa as "empresa_id/id",
'aurb_hdt_delivery_header_'||vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento ||'_aurb_hdt_document' as "documento_id/id",
vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as name,
'aurb_hdt_document_total_'||vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as id
FROM vxx04 inner join v0201 on vxx04.empresa= v0201.empresa 
and vxx04.ejercicio=v0201.ejercicio
and vxx04.almacen = v0201.almacen
and vxx04.tipo_doc = v0201.tipo_doc
and vxx04.documento = v0201.documento
WHERE vxx04.ejercicio='2023' and vxx04.empresa in (select empresa from m0101) 
	 ) to '/tmp/0580aurb.hdt.document.total_albaranes.csv'  header csv delimiter ';'; 

/* 0600 Accounting/subaccount/account entries aurb.hdt.accounting.entries
	(empresa ASC NULLS LAST, asiento ASC NULLS LAST, orden ASC NULLS LAST)
*/
copy(
select apuntes.*,
'aurb_hdt_company_'||apuntes.empresa as "empresa_id/id",
'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as "ejercicio_id/id" ,
'aurb_hdt_subaccounts_'||apuntes.empresa || '_' || coalesce(apuntes.subcta,'') as "sucta_id/id",
'aurb_hdt_currency_' || apuntes.moneda as "moneda_id/id", 
case when length(coalesce(subcta_contrap,'Vacio'))<7 then
		null
else 
	'aurb_hdt_subaccounts_'||apuntes.empresa || '_' || coalesce(apuntes.subcta_contrap,'')
end as "subcta_contrap_id/id",
apuntes.empresa||'_'||apuntes.ejercicio ||'_'||apuntes.asiento ||'_'||'_'||apuntes.orden as name,
'aurb_hdt_accounting_entries_'||apuntes.empresa||'_'||apuntes.ejercicio ||'_'||apuntes.asiento ||'_'||apuntes.orden as id
from apuntes where empresa in (select empresa from m0101) and ejercicio=2023 
)to '/tmp/0600aurb.hdt.accounting.entries.csv' header csv delimiter ';' ENCODING 'UTF-8' ; 

/* 0625
HDT/Configuration/Partners/Partner manual	aurb.hdt.partners.manual.csv
*/
--El índice único es claveman pero se corresponde con empresa, ejercicio,almacen, documento, tipo_documento

	copy (
	SELECT *, 
	'aurb_hdt_company_'||empresa as "empresa_id/Id", 
	'aurb_hdt_partners_'|| empresa || '_' || coalesce(subcta,'') || '_' || coalesce(1,0) as "subcta_id/id",
	'aurb_hdt_warehouses_'||empresa || '_' || coalesce(almacen,'') as "almacen_id/Id",
	'aurb_hdt_accounting_entries_'|| empresa||'_'|| ejercicio ||'_'|| asiento ||'_'|| '1' as "asiento_id/id",
	empresa || '_' || coalesce(ejercicio,0) || '_' ||coalesce(almacen,'0') ||'_'  || coalesce(documento,0) || '_' || coalesce(tipo_doc,'') as name,
	'aurb_hdt_partners_manual_' || empresa || '_' || coalesce(ejercicio,0) || '_' ||coalesce(almacen,'0') ||'_'  || coalesce(documento,0) || '_' || coalesce(tipo_doc,'') as id
	FROM manual where empresa in (select empresa from m0101) and ejercicio=2024
	) to '/tmp/0625aurb.hdt.partners.manual.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;




/* 0655
aurb.hdt.invoice
--'aurb_hdt_accounting_entries_'||v0301.empresa||'_'||v0301.ejercicio ||'_'||v0301.asiento ||'_1' as "asiento_id/id",	
*/
copy ( 
SELECT 
'aurb_hdt_partners_address_' || v0301.empresa || '_' || coalesce(v0301.subcta,'') || '_' || coalesce(v0301.orden,0)||'-'||coalesce(v0301.linea_producto,0) as "adress_id/id",	
'aurb_hdt_accounting_entries_'||v0301.empresa||'_'||v0301.ejercicio ||'_'||v0301.asiento ||'_1' as "asiento_id/id",	
'aurb_hdt_invoice_header_'||V0301.empresa || '_' || V0301.ejercicio || '_' || V0301.almacen || '_' || V0301.tipo_doc || '_' || V0301.documento as id
FROM V0301
JOIN M0101 ON V0301.empresa=M0101.empresa 
WHERE Ejercicio='2023'
 ) to '/tmp/0655aurb.hdt.invoice.header.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/* 0656 Facturas total
aurb.hdt.document.totalalbaranes.csv
*/
-- (empresa ASC NULLS LAST, ejercicio ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, documento ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST)
--aurb_hdt_order_header_1_2023_1_PC_23000013_aurb_hdt_document
copy ( 
SELECT vxx04.*, 
'aurb_hdt_company_'||vxx04.empresa as "empresa_id/id",
'aurb_hdt_invoice_header_'||vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento ||'_aurb_hdt_document' as "documento_id/id",
vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as name,
'aurb_hdt_document_total_'||vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as id
FROM vxx04 inner join v0301 on vxx04.empresa= v0301.empresa 
and vxx04.ejercicio=v0301.ejercicio
and vxx04.almacen = v0301.almacen
and vxx04.tipo_doc = v0301.tipo_doc
and vxx04.documento = v0301.documento
inner join iva on 
iva.asiento=v0301.asiento 
and iva.ejercicio=v0301.ejercicio
and iva.empresa=v0301.empresa	

WHERE vxx04.ejercicio='2023' and vxx04.empresa in (select empresa from m0101) 
	 ) to '/tmp/0656aurb.hdt.document.total_Facturas.csv'  header csv delimiter ';'; 

/*0657
aurb.hdt.document.tax.csv
*/
--(empresa ASC NULLS LAST, asiento ASC NULLS LAST, orden ASC NULLS LAST)
copy ( 
SELECT IVA.*,
'aurb_hdt_company_'||iva.empresa as "empresa_id/id",
IVA.empresa || '_' || IVA.ejercicio || '_' || IVA.asiento || '_' || IVA.orden as name,
--'aurb_hdt_accounting_entries_'||iva.empresa||'_'||iva.ejercicio ||'_'||iva.asiento ||'_1' as "asiento_id/id", --Esto se podría sacar
'aurb_hdt_document_total_'||vxx04.empresa || '_' || vxx04.ejercicio ||'_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as "total_id/id",
'aurb_hdt_document_tax_'||IVA.empresa || '_' || IVA.ejercicio || '_' || IVA.asiento || '_' || IVA.orden as id
FROM vxx04 inner join v0301 on vxx04.empresa= v0301.empresa 
and vxx04.ejercicio=v0301.ejercicio
and vxx04.almacen = v0301.almacen
and vxx04.tipo_doc = v0301.tipo_doc
and vxx04.documento = v0301.documento
inner join iva on 
iva.asiento=v0301.asiento 
and iva.ejercicio=v0301.ejercicio
and iva.empresa=v0301.empresa	
and cast(iva.documento as integer) =v0301.documento
WHERE vxx04.ejercicio='2023' and vxx04.empresa in (select empresa from m0101) 
) to '/tmp/0657aurb.hdt.document.tax.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/*0700
HDT/Payments/Incoming payments original	aurb.hdt.incoming.payments.original.csv
*/
	copy (
	SELECT cobrospdf.*,
	'aurb_hdt_company_'||empresa as "empresa_id/id",
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as "ejercicio_id/id" ,
	'aurb_hdt_currency_' || cobrospdf.moneda as "moneda_id/id", 
	'aurb_hdt_accounting_entries_'||empresa||'_'||ejercicio ||'_'||asientoc ||'_1' as "asiento_id/id",
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as name,
	
	'aurb_hdt_incoming_payments_original_' || coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as id	
	FROM cobrospdf where empresa in (select empresa from m0101) and ejercicio=2023
	) to '/tmp/0700aurb.hdt.incoming.payments.original.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;



--select * from cobrospdf where ejercicio=2024

select documento, asiento, * from vxx04 where ejercicio=2023 limit 200
select documento, asiento, * from iva where ejercicio=2023 limit 100
--x0501

/*
/*Revisar*/
/* 0460
HDT/Configuration/Partners/Partner manual	aurb.hdt.partners.manual.csv
*/
--El índice único es claveman pero se corresponde con empresa, ejercicio,almacen, documento, tipo_documento

	copy (
	SELECT *, 
	'aurb_hdt_company_'||empresa as "empresa_id/Id", 
	'aurb_hdt_partners_'|| empresa || '_' || coalesce(subcta,'') || '_' || coalesce(1,0) as "subcta_id/id",
	'aurb_hdt_warehouses_'||empresa || '_' || coalesce(almacen,'') as "almacen_id/Id",
	empresa || '_' || coalesce(ejercicio,0) || '_' ||coalesce(almacen,'0') ||'_'  || coalesce(documento,0) || '_' || coalesce(tipo_doc,'') as name,
	'aurb_hdt_partners_manual_' || empresa || '_' || coalesce(ejercicio,0) || '_' ||coalesce(almacen,'0') ||'_'  || coalesce(documento,0) || '_' || coalesce(tipo_doc,'') as id
	FROM manual where empresa in (select empresa from m0101)
	) to '/tmp/0460aurb.hdt.partners.manual.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	select * from v0101 limit 100
	
/* 0470
HDT/Payments/Incoming payments	aurb.hdt.incoming.payments.csv
*/
-- (asientoc ASC NULLS LAST, ordenc ASC NULLS LAST, ordenvto ASC NULLS LAST, empresa ASC NULLS LAST)
--		SELECT TO_CHAR(fecha, 'MM.DD.YY') AS fecha_formateada
	copy (
	SELECT empresa, ejercicio, subcta, asientoc, ordenc, asientoliq, ordenliq, 
	to_char(fechaliq,'MM.DD.YY') as fechaliq, 
	documento, ordenvto, 
	to_char(fechavto,'MM.DD.YY') AS fechavto,
	importe, importeb, moneda, cambio, 
	to_char(fechae,'MM.DD.YY') as fechae,
	remesa, 
	to_char(fecharem,'MM.DD.YY') as fecharem, 
	ntalon, tipoe, banco, ordend, comentario, serie, gastosdev, gastosinc, vendedor1, vendedor2, vendedor3, impreso, 
	ccc1, ccc2, dc, numcta, iban, swift, procede, destino, valorc1, valorc2, valord1, valord2,
	
	'aurb_hdt_company_'||empresa as "empresa_id/Id",
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
	'aurb_hdt_currency_'||coalesce(moneda, '') as "moneda_id/id",
	
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as name,
	'aurb_hdt_incoming_payments_' || coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as id	
	FROM cobrosv where empresa in (select empresa from m0101)
	) to '/tmp/0470aurb.hdt.incoming.payments.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	

/* 0480
HDT/Payments/Incoming payments traceability	aurb.hdt.incoming.payments.traceability.csv
*/
	copy (
	SELECT  empresa, ejercicio, subcta, asientoc, ordenc, asientoliq, ordenliq, 
	to_char(fechaliq,'MM.DD.YY') as fechaliq, 
	documento, ordenvto, 
	to_char(fechavto,'MM.DD.YY') AS fechavto,
	importe, importeb, moneda, cambio, 
	to_char(fechae,'MM.DD.YY') as fechae,
	remesa, 
	to_char(fecharem,'MM.DD.YY') as fecharem, 
	ntalon, tipoe, banco, ordend, comentario, serie, gastosdev, gastosinc, vendedor1, vendedor2, vendedor3, impreso, 
	ccc1, ccc2, dc, numcta, iban, swift, procede, destino, valorc1, valorc2, valord1, valord2,
	
	'aurb_hdt_company_'||empresa as "empresa_id/Id",
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
	'aurb_hdt_currency_'||coalesce(moneda, '') as "moneda_id/id",
		
		
		
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as name,
	'aurb_hdt_incoming_payments_traceability_' || coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as id	
	FROM cobrost where empresa in (select empresa from m0101)
	) to '/tmp/0480aurb.hdt.incoming.payments.traceability.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
	
	/* 0490
HDT/Payments/Incoming payments effect	aurb.hdt.incoming.payments.effect.csv
*/
	copy (
	SELECT empresa, ejercicio, subcta, asientoc, ordenc, asientoliq, ordenliq, 
	to_char(fechaliq,'MM.DD.YY') as fechaliq, 
	documento, ordenvto, 
	to_char(fechavto,'MM.DD.YY') AS fechavto,
	importe, importeb, moneda, cambio, 
	to_char(fechae,'MM.DD.YY') as fechae,
	remesa, 
	to_char(fecharem,'MM.DD.YY') as fecharem, 
	ntalon, tipoe, banco, ordend, comentario, serie, gastosdev, gastosinc, vendedor1, vendedor2, vendedor3, impreso, 
	ccc1, ccc2, dc, numcta, iban, swift, procede, destino, valorc1, valorc2, valord1, valord2,
	
	'aurb_hdt_company_'||empresa as "empresa_id/Id",
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
	'aurb_hdt_currency_'||coalesce(moneda, '') as "moneda_id/id",
	
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as name,
	'aurb_hdt_incoming_payments_effect_' || coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as id	
	FROM cobrosm where empresa in (select empresa from m0101)
	) to '/tmp/0490aurb.hdt.incoming.payments.effect.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
	
	/* 0500
HDT/Payments/Incoming payments original	aurb.hdt.incoming.payments.original.csv
*/
	copy (
	SELECT empresa, ejercicio, subcta, asientoc, ordenc, asientoliq, ordenliq, 
	to_char(fechaliq,'MM.DD.YY') as fechaliq, 
	documento, ordenvto, 
	to_char(fechavto,'MM.DD.YY') AS fechavto,
	importe, importeb, moneda, cambio, 
	to_char(fechae,'MM.DD.YY') as fechae,
	remesa, 
	to_char(fecharem,'MM.DD.YY') as fecharem, 
	ntalon, tipoe, banco, ordend, comentario, serie, gastosdev, gastosinc, vendedor1, vendedor2, vendedor3, impreso, 
	ccc1, ccc2, dc, numcta, iban, swift, procede, destino, valorc1, valorc2, valord1, valord2,
	
	'aurb_hdt_company_'||empresa as "empresa_id/Id",
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
	'aurb_hdt_currency_'||coalesce(moneda, '') as "moneda_id/id",
	
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as name,
	'aurb_hdt_incoming_payments_original_' || coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0)|| '_' || coalesce(ordenvto,0) as id	
	FROM cobrospdf where empresa in (select empresa from m0101)
	) to '/tmp/0500aurb.hdt.incoming.payments.original.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;


/* 0510
HDT/Stock/Stock transfer	aurb.hdt.stock.transfer.csv
*/
--(empresa ASC NULLS LAST, tipo_doc COLLATE pg_catalog."default" ASC NULLS LAST, documento ASC NULLS LAST)
	copy (
	SELECT empresa, ejercicio, almacen_o, almacen_d, n_produccion, documento, 
	to_char(fecha_documento, 'MM.DD.YY') as fecha_documento,
	tipo_doc, situacion, 
	to_char(fecha_entrada,'MM.DD.YY') as fecha_entrada, 
	usuario_entrada, hora_entrada, 
	to_char(fecha_modifi,'MM.DD.YY') AS fecha_modif, 
	usuario_modifi, hora_modifi, asiento, 
	
	'aurb_hdt_company_'||coalesce(empresa,0) as "empresa_id/id", 
	'aurb_hdt_warehouses_'||coalesce(empresa,0) ||coalesce(almacen_o,'') as "almacen_o_id/id", 
	'aurb_hdt_warehouses_'||coalesce(empresa,0) ||coalesce(almacen_d,'') as "almacen_d_id/id",
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
	
	coalesce(empresa,0) || '_' || coalesce(tipo_doc, '') || '_' || coalesce(documento, 0) as name,
	'aurb_hdt_stock_transfer_' || coalesce(empresa,0) || '_' || coalesce(tipo_doc, '') || '_' || coalesce(documento, 0) as id	
	FROM v0401 where empresa in (select empresa from m0101)
	) to '/tmp/0510aurb.hdt.stock.transfer.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
	/* 0520
HDT/Stock/Stock transfer lines	aurb.hdt.stock.transfer.lines.csv
*/
	copy (
	SELECT empresa, ejercicio, tipo_movimiento, documento, linea_trs, clv_trs, articulo, clv_art, cantidad, bultos, precio_o, precio_d, total_linea_o, 
	total_linea_o_base, total_linea_o_euro, total_linea_d, total_linea_d_base, total_linea_d_euro, moneda_o, moneda_d, cambio_o, cambio_o_euro, cambio_d,
	cambio_d_euro, almacen_o, almacen_d, 
	to_char(fecha_documento,'MM.DD.YYYY') AS fecha_documento, 
	triangulado_o, triangulado_d, lote_interno, 
	'aurb_hdt_company_'||coalesce(empresa,0) as "empresa_id/id", 
	'aurb_hdt_stock_transfer_' || coalesce(empresa,0) || '_' || coalesce(tipo_movimiento, '') || '_' || coalesce(documento, 0) as id,
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
		
	moneda_o as moneda_o_id,moneda_d as moneda_d_id,
	coalesce(empresa,0) || '_' || coalesce(tipo_movimiento, '') || '_' || coalesce(documento, 0) || '_' || coalesce(linea_trs, 0)   as name
	FROM v040101 where empresa in (select empresa from m0101)
	) to '/tmp/0520aurb.hdt.stock.transfer.lines.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;
	
	/* 0530
HDT/Stocks/Manufacturing orders filter	aurb.hdt.manufacturing.orders.csv
 empresa_id = fields.Many2one("aurb.hdt.company")
 ejercicio_id = fields.Many2one("aurb.hdt.exercices")
 almacen_id = fields.Many2one("aurb.hdt.warehouse")
*/

	-- (empresa ASC NULLS LAST, ejercicio ASC NULLS LAST, almacen COLLATE pg_catalog."default" ASC NULLS LAST, documento_sf ASC NULLS LAST, documento_ef ASC NULLS LAST)
	copy (
	SELECT empresa, ejercicio, almacen, 
	to_char(fecha_sf,'MM.DD.YY') AS fecha_sf, 
	to_char(fecha_ef,'MM.DD.YY') as fecha_ef, 
	documento_sf, documento_ef, lote, subcta_c, subcta_s, pedido, linea_pedido, articulo, 
	cantidad_sf, cantidad_ef, observaciones, n_traspaso, estado, of_original, 
	'aurb_hdt_company_'||coalesce(empresa,0) as "empresa_id/id", 
	'aurb_hdt_warehouses_'||coalesce(empresa,0) ||'_'||coalesce(almacen,'') as "almacen_id/id", 
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
	coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento_sf, 0) || '_' || coalesce(documento_ef,0) as name,
	'aurb_hdt_manufacturing_orders_' || coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento_sf, 0)  as id	
	FROM v0501
	where ejercicio=2023  and empresa in (select empresa from m0101)
	) to '/tmp/0530aurb.hdt.manufacturing.orders.csv'  header csv delimiter ';' ENCODING 'UTF-8' ;

/* 0540
HDT/Stocks/Manufacturing order lines	aurb.hdt.manufacturing.order.lines.csv
*/
 --(*documento ASC NULLS LAST, tipo_movimiento COLLATE pg_catalog."default" ASC NULLS LAST, *almacen COLLATE pg_catalog."default" ASC NULLS LAST, *ejercicio ASC NULLS LAST, *empresa ASC NULLS LAST, linea_documento ASC NULLS LAST)
	copy (
	SELECT empresa, ejercicio, almacen, documento, 
	to_char(fecha_documento,'MM.DD.YY') AS fecha_documento, 
	linea_documento, tipo_movimiento, subcta_c, subcta_s, pedido, fase, codigo, articulo, clv_art, cantidad, bultos, precio, precio_coste, 
	moneda, cambio, cambio_euro, impresa, 
	to_char(fecha_entrada,'MM.DD.YY') AS fecha_entrada, 
	usuario_entrada, hora_entrada, 
	to_char(fecha_modifi,'MM.DD.YY') AS fecha_modifi, 
	usuario_modifi, hora_modifi, acumula, 
	base, lote_interno, campo1, campo2, 
	
	'aurb_hdt_company_'||coalesce(empresa,0) as "empresa_id/id", 
	'aurb_hdt_warehouses_'||coalesce(empresa,0) ||'_'||coalesce(almacen,'') as "almacen_id/id",
	'aurb_hdt_fiscal_year_' || coalesce(empresa,0) || '_' || coalesce(ejercicio,0)  as "ejercicio_id/id",
	'aurb_hdt_manufacturing_orders_' || coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento, 0)  as "documento_id/Id",	
		
	coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento, 0) || '_' || coalesce(tipo_movimiento,'x') || '_' || coalesce(linea_documento,0) as name,
	'aurb_hdt_manufacturing_orders_lines_' || coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento, 0) || '_' || coalesce(tipo_movimiento,'x') || '_' || coalesce(linea_documento,0) as id
	FROM v050101
	where ejercicio=2023 and empresa in (select empresa from m0101) 
	and 'aurb_hdt_manufacturing_orders_' || coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento, 0)
	not in ('aurb_hdt_manufacturing_orders_1_2023_1_23000001','aurb_hdt_manufacturing_orders_1_2023_1_23000002', 'aurb_hdt_manufacturing_orders_1_2023_1_23000003','aurb_hdt_manufacturing_orders_1_2023_1_23000004')
	) to '/tmp/0540aurb.hdt.manufacturing.orders_lines.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;
/*Fin Revisar*/
/*
 select distinct empresa from v050101
  
select * from v050101 where  documento = 23000001

select distinct documento from v050101 where v050101.empresa = 1  and ejercicio=2023 and tipo_movimiento = 'SF' and
 v050101.documento  in (select documento_sf from v0501 where empresa = 1)  order by 1
*/

