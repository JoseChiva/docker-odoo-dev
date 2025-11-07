{
    'name': 'gamma_integration',
    'version': '18.1.5',
    'depends': [
        'base',
        'sale_management',
        'stock', 'web'
    ],
    'category': 'Tools',
    'summary': 'Web services Gamma Integration',
    'description': "Gamma Integration",
    'author': 'Jose Luis Chiva',
    'website': '',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/gamint_settings_view.xml',
        'views/gamint_config_settings_view.xml',
        'views/gamint_product_template_view.xml',
        'views/gamint_sale_order_head_view.xml',
        'views/gamint_sale_order_line_view.xml',
        'data/gamint_gamma_cron.xml',
    ],
    'license': 'LGPL-3',
}
