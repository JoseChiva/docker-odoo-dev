{
    'name': "partner_commission_extended",
    'version': '18.1.1',
    'depends': ['base', 'sale', 'partner_commission',],
    'category': 'Category',
    'description': "Módulo de extensión de comisión de Odoo",
    'website': 'https://auren.com/es/',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/auren_sale_order_form.xml',
        'views/auren_res_partner.xml',
    ],
    'license': 'LGPL-3',
}
