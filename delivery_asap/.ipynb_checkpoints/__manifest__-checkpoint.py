# -*- coding: utf-8 -*-
{
    'name': "delivery_asap",

    'summary': """
        """,

    'description': """
        Integración con ASAP para la generación de envios desde E-commerce.
    """,

    'author': "THAVAS",
    'website': "http://www.thavasconsultoria.com/odoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Delivery',
    'version': '15.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','website','delivery'],

    # always loaded
    'data': [
        'views/stock_picking_inherited.xml',
        'views/delivery_inherited.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
