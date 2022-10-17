# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BAC CREDOMATIC Payment Acquirer',
    'version': '15.0.1',
    'category': 'Accounting/Payment Acquirers',
    'description': """
PAsarela de Pago BAC CREDOMATIC
""",
    'author': "THAVAS",
    'website': "http://www.thavasconsultoria.com/odoo",

    'depends': ['website_sale','payment','website'],
    'data': [
        'views/payment_view.xml',
        'views/payment_bac_templates.xml',
        'data/payment_acquirer_data.xml',
        'views/templates.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_bac/static/src/js/**/*',
        ],
    },
    'license': 'LGPL-3',
}
