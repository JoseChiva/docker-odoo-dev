/* 
HDT/Configuration/Empresas	aurb.hdt.company.csv
*/
	copy (
	SELECT *, empresa as name
	FROM m0101
	union all
	SELECT 0 as empresa,'Sin empresa','','',0,0,0,'','',0
	) to '/tmp/aurb.hdt.company.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/* 
HDT/Configuration/Warehouse	aurb.hdt.warehouses.csv
*/

	copy (
	SELECT *, empresa as empresa_id, 
	empresa || '_' || almacen as name
	FROM m0401 
	) to '/tmp/aurb.hdt.warehouses.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;
	

/* 
HDT/Configuration/Currency/Currency	aurb.hdt.currency.csv
*/

	copy (
	SELECT *, 
	moneda as name
	FROM x1301
	) to '/tmp/aurb.hdt.currency.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;
	
	
/* 
HDT/Configuration/Vehicle	aurb.hdt.vehicles.csv
*/

	copy (
	SELECT *, 
	codigo as name
	FROM m0601
	) to '/tmp/aurb.hdt.vehicles.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Exerercises	aurb.hdt.fiscal.year.csv
*/

	copy (
	SELECT *, 
	coalesce(empresa,0) as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as name
	FROM ejercicios
	) to '/tmp/aurb.hdt.fiscal.year.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Language	aurb.hdt.language.csv
*/

	copy (
	SELECT *, 
	coalesce(idioma, 0) as name
	FROM x2001
	) to '/tmp/aurb.hdt.language.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Countrys/Country	aurb.hdt.country.csv
*/

	copy (
	SELECT *, pais as name
	FROM x0601 
	) to '/tmp/aurb.hdt.country.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Countrys/Country Ce	aurb.hdt.country.ce.csv
*/

/* 
HDT/Configuration/Currency/Currency subaccount	aurb.hdt.currency.subaccount.csv
*/

	copy (
	SELECT *, 
	moneda as moneda_id,
	moneda_ref || '_' || moneda as name
	FROM x1302
	) to '/tmp/aurb.hdt.currency.subaccount.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Currency/Currency change	aurb.hdt.currency.change.csv
*/
	copy (
	SELECT *, 
	moneda as moneda_id,
	moneda_ref || '_' || moneda || '_' || fecha_inicio as name
	FROM x1303
	) to '/tmp/aurb.hdt.currency.change.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/* 
HDT/Configuration/Banks/Bank	aurb.hdt.bank.csv
*/

	copy (
	SELECT *, 
	empresa as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(subcta, '') as name
	FROM bancos
	) to '/tmp/aurb.hdt.bank.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Accounting/Subaccounts	aurb.hdt.subaccounts.csv
*/

	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as name
	FROM subcuentas
	) to '/tmp/aurb.hdt.subaccounts.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Banks/Bank (more info)	aurb.hdt.bank01.csv
*/

	copy (
	SELECT *, empresa as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(subcta, '') as subcta_id,
	coalesce(empresa,0) || '_' || coalesce(iban,'') as name
	FROM bancos01
	) to '/tmp/aurb.hdt.bank01.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Banks/Bank entity	aurb.hdt.bank.ent.csv
*/

	copy (
	SELECT *, 
	coalesce(ccc1,'') as name
	FROM x1701
	) to '/tmp/aurb.hdt.bank.ent.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Banks/Bank office	aurb.hdt.bank.ofi.csv
*/

	copy (
	SELECT *, 
	coalesce(ccc1,'') as ccc1_id,
	coalesce(ccc1,'') || '_' || coalesce(ccc2,'') as name
	FROM x170101
	) to '/tmp/aurb.hdt.bank.ofi.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/* 
HDT/Configuration/Warehouse currency	aurb.hdt.warehouses.currency.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id,
	m0402.empresa || '_' || m0402.almacen as almacen_id,
	m0402.moneda_ref as moneda_ref_id,
	m0402.moneda_cons as moneda_cons_id,
	m0402.empresa || '_' || m0402.almacen || '_' || m0402.moneda_ref as name
	FROM m0402 
	) to '/tmp/aurb.hdt.warehouses.currency.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Configuration/Sellers/Seller	aurb.hdt.sellers.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(subcta,'') as name
	FROM m0501
	) to '/tmp/aurb.hdt.sellers.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Configuration/Sellers/Seller commision	aurb.hdt.sellers.commissions.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	coalesce(empresa,0) || '_' || coalesce(subcta,'') || '_' || coalesce(codigo,'') as name
	FROM m050101
	) to '/tmp/aurb.hdt.sellers.commissions.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Configuration/Sellers/Seller cumulative	aurb.hdt.sellers.accumulated.sales.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	moneda as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(subcta,'') as name
	FROM m0502
	) to '/tmp/aurb.hdt.sellers.accumulated.sales.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Configuration/Sellers/Seller cumulative	aurb.hdt.sellers.accumulated.sales.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	moneda as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(subcta,'') as name
	FROM m0502
	) to '/tmp/aurb.hdt.sellers.accumulated.sales.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Configuration/Partners/Partner	aurb.hdt.partners.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id,
	empresa || '_' || coalesce(subcta_contable,'') as subcta_contable_id,
	empresa || '_' || coalesce(subcta_facturacion,'') as subcta_facturacion_id,
	empresa || '_' || coalesce(subcta,'') as name
	FROM m0201
	) to '/tmp/aurb.hdt.partners.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Configuration/Partners/Partner card	aurb.hdt.partners.card.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	empresa || '_' || coalesce(subcta,'') || '_' || coalesce(num_tarjeta,'') as name
	FROM m020102
	) to '/tmp/aurb.hdt.partners.card.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Configuration/Partners/Partner risk	aurb.hdt.partners.risk.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	moneda as moneda_id,
	empresa || '_' || coalesce(subcta,'')  as subcta_id,
	empresa || '_' || coalesce(subcta,'') || '_' || coalesce(moneda,'') as name
	FROM m0202
	) to '/tmp/aurb.hdt.partners.risk.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Configuration/Partners/Partner payment terms	aurb.hdt.partners.pay.terms.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	coalesce(ccc1,'') || '_' || coalesce(ccc2,'') as ccc1_id,
	coalesce(ccc1,'') as ccc2_id,
	coalesce(ccc1,'') as swift_id,
	empresa || '_' || coalesce(subcta,'') as name
	FROM m0204
	) to '/tmp/aurb.hdt.partners.pay.terms.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Configuration/Partners/Partner account	aurb.hdt.partners.account.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	empresa || '_' || coalesce(subcta,'') as name
	FROM m0206
	) to '/tmp/aurb.hdt.partners.account.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Configuration/Partners/Partner contact	aurb.hdt.partners.contact.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	empresa || '_' || coalesce(subcta,'') || '_' || coalesce(contacto,'') as name
	FROM m0208
	) to '/tmp/aurb.hdt.partners.contact.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Configuration/Partners/Partner comments	aurb.hdt.partners.comments.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	empresa || '_' || coalesce(subcta,'') || '_' || coalesce(tipo_obs,0) || '_' || coalesce(numero_obs,0) as name
	FROM m0209
	) to '/tmp/aurb.hdt.partners.comments.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Configuration/Partners/Partner address	aurb.hdt.partners.address.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	empresa || '_' || coalesce(subcta,'') || '_' || coalesce(orden,0) as name
	FROM direcciones
	) to '/tmp/aurb.hdt.partners.address.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Configuration/Partners/Partner manual	aurb.hdt.partners.manual.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || coalesce(almacen,'') as almacen_id,
	empresa || '_' || coalesce(subcta,'') as subcta_id,
	empresa || '_' || coalesce(ejercicio,0) || '_' || coalesce(documento,0) || '_' || coalesce(subcta,'') as name
	FROM manual
	) to '/tmp/aurb.hdt.partners.manual.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Payments/Incoming payments	aurb.hdt.incoming.payments.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
	FROM cobrosv
	) to '/tmp/aurb.hdt.incoming.payments.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Payments/Incoming payments traceability	aurb.hdt.incoming.payments.traceability.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
	FROM cobrost
	) to '/tmp/aurb.hdt.incoming.payments.traceability.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Payments/Incoming payments effect	aurb.hdt.incoming.payments.effect.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
	FROM cobrosm
	) to '/tmp/aurb.hdt.incoming.payments.effect.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Payments/Incoming payments original	aurb.hdt.incoming.payments.original.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
	FROM cobrospdf
	) to '/tmp/aurb.hdt.incoming.payments.original.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Payments/Outcoming payments	aurb.hdt.outcoming.payments.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
	FROM cobrospdf
	) to '/tmp/aurb.hdt.incoming.payments.original.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Payments/Outcoming payments traceability	aurb.hdt.outcoming.payments.traceability.csv
*/

/*
HDT/Payments/Outcoming payments effect	aurb.hdt.outcoming.payments.effect.csv
*/

/*
HDT/Payments/Outcoming payments TPV	aurb.hdt.outcoming.payments.tpv.csv
*/

/*
HDT/Stock/Stock transfer	aurb.hdt.stock.transfer.csv
*/
	copy (
	SELECT *, 
	coalesce(empresa,0) as empresa_id, 
	coalesce(almacen_o,'') as almacen_o_id, 
	coalesce(almacen_d,'') as almacen_d_id, 
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(empresa,0) || '_' || coalesce(tipo_doc, '') || '_' || coalesce(documento, 0) as name
	FROM v0401
	) to '/tmp/aurb.hdt.stock.transfer.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Stock/Stock transfer lines	aurb.hdt.stock.transfer.lines.csv
*/
	copy (
	SELECT *, 
	coalesce(empresa,0) as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(tipo_movimiento, '') || '_' || coalesce(documento, 0) as documento_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	moneda_o as moneda_o_id,moneda_d as moneda_d_id,
	coalesce(empresa,0) || '_' || coalesce(tipo_movimiento, '') || '_' || coalesce(documento, 0) || '_' || coalesce(linea_trs, 0)   as name
	FROM v040101
	) to '/tmp/aurb.hdt.stock.transfer.lines.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Stocks/Manufacturing orders filter	aurb.hdt.manufacturing.orders.csv
*/
	copy (
	SELECT *, 
	coalesce(empresa,0) as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(almacen,'') as almacen_id, 
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento_sf, 0) as name
	FROM v0501
	where ejercicio=2023
	) to '/tmp/aurb.hdt.manufacturing.orders.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Stocks/Manufacturing order lines	aurb.hdt.manufacturing.order.lines.csv
*/
	copy (
	SELECT *, 
	coalesce(empresa,0) as empresa_id, 
	coalesce(empresa,0) || '_' || coalesce(almacen,'') as almacen_id, 
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio, 0) || '_' || coalesce(almacen, '') || '_' || coalesce(documento_sf, 0) as name
	FROM v0501
	where ejercicio=2023
	) to '/tmp/aurb.hdt.manufacturing.orders.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/POS/POS	aurb.hdt.pos.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) as name
	FROM tpx04
	) to '/tmp/aurb.hdt.pos.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/POS/Payment method	aurb.hdt.pos.payment.method.csv
*/
	copy (
	SELECT *, 
	coalesce(codigo_pago,0) as name
	FROM tpx01
	) to '/tmp/aurb.hdt.pos.payment.method.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/POS/Account payment method	aurb.hdt.pos.account.payment.method.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(almacen,'') as almacen_id, 
	coalesce(codigo_pago,0) as codigo_pago_id,
	coalesce(empresa,0) || '_' || coalesce(subcta, '') as subcta_id,
	coalesce(empresa,0) || '_' || coalesce(almacen,'') || '_' || coalesce(codigo_pago,0) as name
	FROM tpx02
	) to '/tmp/aurb.hdt.pos.account.payment.method.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/POS/Assignment	aurb.hdt.pos.assignment.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(subcta_contado_s,'') as subcta_contado_s_id,
	coalesce(empresa,0) || '_' || coalesce(subcta_contado_n,'') as subcta_contado_n_id,
	coalesce(empresa,0) || '_' || coalesce(subcta_caja,'') as subcta_caja_id,
	coalesce(empresa,0) || '_' || coalesce(subcta_pendte,'') as subcta_pendte_id,
	coalesce(idioma_1,0) as idioma_1_id,
	coalesce(idioma_2,0) as idioma_2_id,
	coalesce(idioma_auxiliar,0) as idioma_auxiliar_id,
	coalesce(empresa,0) || '_' || coalesce(usuario,'') || '_' || coalesce(tpv,0) as name
	FROM tpx03
	) to '/tmp/aurb.hdt.pos.assignment.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/POS/Payment method by POS	aurb.hdt.pos.payment.method.by.pos.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(codigo_pago,0) as codigo_pago_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) || '_' || coalesce(codigo_pago,0) as name
	FROM tpx0301
	) to '/tmp/aurb.hdt.pos.payment.method.by.pos.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/POS/Default printer	aurb.hdt.default.printer
*/
copy (
SELECT *,
coalesce(empresa,0) as empresa_id,
coalesce(empresa,0) || '_' || coalesce(usuario, '') || '_' || coalesce(tipo_doc, '') || '_' || coalesce(impresora, '') as name
FROM tpx0401
) to '/tmp/aurb.hdt.default.printer.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/POS/POS Documents	aurb.hdt.pos.documents.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(empresa,0) || '_' || coalesce(almacen, '') as almacen_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) as tpv_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) as name
	FROM tpv01
	) to '/tmp/aurb.hdt.pos.documents.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/POS/POS Collections	aurb.hdt.pos.collections.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(empresa,0) || '_' || coalesce(almacen, '') as almacen_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) as tpv_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) as name
	FROM tpv01
	) to '/tmp/aurb.hdt.pos.documents.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/POS/POS Cumulative	aurb.hdt.pos.cumulative.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
	coalesce(empresa,0) || '_' || coalesce(almacen, '') as almacen_id,
	coalesce(moneda, '') as moneda_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) as tpv_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) || '_' || fecha as name
	FROM tpv03
	) to '/tmp/aurb.hdt.pos.cumulative.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/POS/POS cash count	aurb.hdt.pos.cash.count.csv
*/
	copy (
	SELECT *,
	coalesce(empresa,0) as empresa_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) as tpv_id,
	coalesce(empresa,0) || '_' || coalesce(tpv,0) || '_' || fecha as name
	FROM tpvarqueo
	) to '/tmp/aurb.hdt.pos.cash.count.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Items/Item	aurb.hdt.items.csv
*/
	copy (
	SELECT *, empresa as empresa_id, empresa || '_' || codigo as name
	FROM m0301
	) to '/tmp/aurb.hdt.items.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Items/Item desc	aurb.hdt.items.description.csv
*/
	copy (
	SELECT *, empresa as empresa_id, 
	empresa || '_' || codigo as codigo_id,
	empresa || '_' || codigo || '_' || descripcion as name
	FROM m0302
	) to '/tmp/aurb.hdt.items.description.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Items/Item Price	aurb.hdt.items.price.csv
*/
	copy (
	SELECT *, coalesce(empresa, 0) as empresa_id, 
	coalesce(empresa, 0) || '_' || codigo as codigo_id,
	moneda as moneda_id,
	coalesce(empresa, 0) || '_' || codigo || '_' || variante as name
	FROM m0303
	) to '/tmp/aurb.hdt.items.price.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;



/*
HDT/Items/Item batch	aurb.hdt.items.batch.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || almacen as almacen_id,
	empresa || '_' || almacen || '_' || codigo as codigo_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno as name
	FROM m0319
	) to '/tmp/aurb.hdt.items.batch.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Items/Items batch piece	aurb.hdt.items.batch.piece.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || almacen as almacen_id,
	empresa || '_' || almacen || '_' || codigo as codigo_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno as lote_interno_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno || '_' || npieza as name	
	FROM m031901
	) to '/tmp/aurb.hdt.items.batch.piece.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Items/Item batch incident	aurb.hdt.items.batch.incident.csv
*/
	copy (
	SELECT *, 
	empresa as empresa_id, 
	empresa || '_' || almacen as almacen_id,
	empresa || '_' || almacen || '_' || codigo as codigo_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno as lote_interno_id,
	empresa || '_' || almacen || '_' || codigo || '_' || lote_interno || '_' || incidencia as name
	FROM m031903
	) to '/tmp/aurb.hdt.items.batch.incident.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Sales/ Sales Order/Sales Order Head	aurb.hdt.order.header.csv
*/
	copy ( 
	SELECT v0101.*,
	v0101.empresa as empresa_id,
	v0101.empresa || '_' || v0101.almacen as almacen_id, 
	
	v0101.empresa || '_' || v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento as name 
	FROM v0101
	WHERE Ejercicio='2023'
	 ) to '/tmp/aurb.hdt.order.header.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Sales/ Sales Order/Sales Order Lines	aurb.hdt.order.lines.csv
*/
	copy ( 
	SELECT v010101.*,
	v0101.empresa as empresa_id,
	v010101.moneda as moneda_id,
	v0101.empresa || '_' || v0101.almacen as almacen_id, 
	v0101.empresa || '_' || v010101.articulo as articulo_id, 
	v0101.empresa || '_' || v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento as pedido_id,
	v0101.empresa || '_' || v0101.almacen || '_' || v0101.tipo_doc || '_' || v0101.documento || '_' || v010101.linea_pedido as name
	FROM v0101
	JOIN v010101 ON v0101.empresa=v010101.empresa and v0101.ejercicio=v010101.ejercicio and 
	v0101.tipo_doc=v010101.tipo_movimiento and 
	v0101.documento=v010101.pedido and
	v0101.almacen=v010101.almacen
	WHERE v0101.ejercicio='2023' 
	 ) to '/tmp/aurb.hdt.order.lines.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;		

/*
HDT/Sales/ Sales Order/Sales Order Manual Description	aurb.hdt.order.man.description.csv
*/
	copy ( 
	SELECT vxxxx01.*,
	vxxxx01.empresa as empresa_id,
	vxxxx01.empresa || '_' || vxxxx01.almacen as almacen_id, 
	vxxxx01.empresa || '_' || vxxxx01.almacen || '_' || vxxxx01.tipo_doc || '_' || vxxxx01.documento as documento_id,
	vxxxx01.empresa || '_' || vxxxx01.almacen || '_' ||  vxxxx01.tipo_doc || '_' || vxxxx01.documento || '_' || vxxxx01.orden || '_' || vxxxx01.almacen as name
	FROM vxxxx01
	WHERE vxxxx01.ejercicio='2023'
	 ) to '/tmp/aurb.hdt.order.man.description.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Sales/Delivery/Sales Delivery Head	aurb.hdt.delivery.header.csv
*/
copy ( 
SELECT V0201.*,
V0201.empresa as empresa_id,
v0201.moneda as moneda_id,
V0201.empresa || '_' || V0201.almacen as almacen_id, 

V0201.empresa || '_' || V0201.almacen || '_' || V0201.tipo_doc || '_' || V0201.documento as name 
FROM V0201
JOIN M0101 ON V0201.empresa=M0101.empresa
WHERE Ejercicio='2023'
 ) to '/tmp/aurb.hdt.delivery.header.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Sales/Delivery/Sales Delivery Lines	aurb.hdt.delivery.lines.csv
*/
	copy ( 
	SELECT v020101.*,
	v0201.empresa as empresa_id,
	v020101.moneda as moneda_id,
	v0201.empresa || '_' || v0201.almacen as almacen_id, 
	V0201.empresa || '_' || v020101.articulo as articulo_id, 
	v0201.empresa || '_' || v0201.almacen || '_' || v0201.tipo_doc || '_' || v0201.documento as albaran_id,
	v0201.empresa || '_' || v0201.almacen || '_' || CASE v0201.tipo_doc WHEN 'EC' THEN 'FC' WHEN 'SV' THEN 'FV' END || '_' || v0201.factura as factura_id,
	v0201.empresa || '_' || v0201.almacen || '_' || v0201.tipo_doc || '_' || v0201.documento || '_' || v020101.linea_albaran as name
	FROM v0201
	JOIN v020101 ON v0201.empresa=v020101.empresa and v0201.ejercicio=v020101.ejercicio and 
	v0201.tipo_doc=v020101.tipo_movimiento and 
	v0201.documento=v020101.albaran and
	v0201.almacen=v020101.almacen
	WHERE v0201.ejercicio='2023' 
	 ) to '/tmp/aurb.hdt.delivery.lines.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;


/*
HDT/Payments/Outcoming payments	aurb.hdt.outcoming.payments.csv
*/

copy (
SELECT *,
coalesce(empresa,0) as empresa_id,
coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
coalesce(moneda, '') as moneda_id,
coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
FROM pagosv
) to '/tmp/aurb.hdt.outcoming.payments.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Payments/Outcoming payments traceability	aurb.hdt.outcoming.payments.traceability.cs
*/

copy (
SELECT *,
coalesce(empresa,0) as empresa_id,
coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
coalesce(moneda, '') as moneda_id,
coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
FROM pagost
) to '/tmp/aurb.hdt.outcoming.payments.traceability.cs'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Payments/Outcoming payments effect	aurb.hdt.outcoming.payments.effect.csv
*/

copy (
SELECT *,
coalesce(empresa,0) as empresa_id,
coalesce(empresa,0) || '_' || coalesce(ejercicio,0) as ejercicio_id,
coalesce(moneda, '') as moneda_id,
coalesce(empresa,0) || '_' || coalesce(asientoc,0) || '_' || coalesce(ordenc,0) as name
FROM pagosm 
) to '/tmp/aurb.hdt.outcoming.payments.effect.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*
HDT/Payments/Outcoming payments TPV	aurb.hdt.outcoming.payments.tpv.csv
*/


copy (
SELECT *,
coalesce(empresa,0) as empresa_id,
coalesce(empresa,0) || '_' || coalesce(asiento,0) || '_' || coalesce(tpv,0) as name
FROM pagostpv 
) to '/tmp/aurb.hdt.outcoming.payments.tpv.csv'  header csv delimiter ',' ENCODING 'UTF-8' ;

/*

*/
copy ( 
SELECT vxx04.*,
vxx04.empresa as empresa_id,
vxx04.empresa || '_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as document_id,
vxx04.empresa || '_' || vxx04.almacen || '_' || vxx04.tipo_doc || '_' || vxx04.documento as name
FROM vxx04
WHERE vxx04.ejercicio='2023' 
	 ) to '/tmp/aurb.hdt.document.total.csv'  header csv delimiter ',' ENCODING 'UTF-8' ; 


copy ( 
SELECT IVA.*,
IVA.empresa as empresa_id,
IVA.empresa || '_' || IVA.ejercicio || '_' || IVA.asiento || '_' || IVA.documento as document_id,
IVA.empresa || '_' || IVA.ejercicio || '_' || IVA.asiento || '_' || IVA.documento as name
FROM IVA
WHERE IVA.ejercicio='2023' 
	 ) to '/tmp/aurb.hdt.document.tax.csv'  header csv delimiter ',' ENCODING 'UTF-8'; 