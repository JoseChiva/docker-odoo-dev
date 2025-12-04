{
    'name': "journal_warehouse",
    'version': '17.1.2',
    'depends': ['base', 'product', 'stock', 'account', 'account_accountant',],
    'category': 'Category',
    'description': "Modulo de asignación de diario al almacén",
    'website': 'https://auren.com/es/',
    'installable': True,
    'application': False,
    'auto_install': False,
    'data': [
        'views/auren_jouwar_res_config_settings_views.xml',
        'views/auren_jouwar_location.xml',
    ],
    'license': 'LGPL-3',
}
