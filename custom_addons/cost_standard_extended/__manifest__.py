{
    'name': 'cost_standard_extended',
    'version': '18.1.1',
    'depends': [
        'base',
        'stock',
    ],
    'category': 'Category',
    'description': "Extensión de coste estandard",
    'website': '',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/auren_otools_group_security.xml',
        'security/ir.model.access.csv',
        'views/aurb_cst_cost_standard.xml',
        'views/aurb_cst_res_config_settings_views.xml',
        'views/aurb_cst_product_template.xml'
    ],
    'license': 'LGPL-3',
}
