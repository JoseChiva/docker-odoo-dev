{
    'name': 'multi_discount_sale',
    'version': '18.1.3',
    'depends': [
        'base',
        'sale',
    ],
    'category': 'Category',
    'description': "Modulo multi descuento de ventas",
    'website': '',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/auren_otools_group_security.xml',
        'security/ir.model.access.csv',
        'views/auren_mds_sales_res_partners_view.xml',
        'views/auren_mds_sales_sale_order_view.xml',
        'views/auren_mds_res_config_settings_views.xml',
        'views/auren_mds_account_move_view.xml',
    ],
    'license': 'LGPL-3',
}
