# -*- coding: utf-8 -*-
{
    'name': "Etiquetas_pos",

    'summary': """
Generad/modifica etiquetas para el POS""",

    'description': """
        
    """,

    'author': "THAVAS",
    'website': "http://www.thavasconsultoria.com/odoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Point of Sale',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'etiquetas_pos/static/src/js/*',
        ],
         'web.assets_qweb': [
             'etiquetas_pos/static/src/xml/OrderSummary_Inherited.xml'
        ],
    },


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    
    'license': 'LGPL-3',
}
