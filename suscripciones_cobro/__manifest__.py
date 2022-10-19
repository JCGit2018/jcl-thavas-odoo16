# -*- coding: utf-8 -*-
{
    'name': 'Cobro suscripciones ODOO',
    'depends': ['base',
        'sale_management',
        'portal',
        'web_cohort',
        'rating',
        'base_automation',
        'sms',
        'sale_subscription',
    ],
    'data': [
        #'views/payment_view.xml',
        #'views/payment_cybersource_template.xml',
        #'data/payment_acquirer_data.xml',
    ],
    'images': ['static/description/cyber_source_logo.jpg'],
    'auto_install': False,
    'author': "THAVAS",
    'website': "http://www.thavasconsultoria.com/odoo",

    'category': 'Sales',
    'version': '16.0.1',
}

