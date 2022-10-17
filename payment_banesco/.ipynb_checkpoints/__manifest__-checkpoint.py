# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Conector Pago Banesco',
    'author': "THAVAS",
    'website': "http://www.thavasconsultoria.com/odoo",

    'version': '15.0.1.1',
    'category': 'Accounting/Payment Acquirers',
    'description': """
    Pasarela de Pago Cybersource Banesco para ODOO
    """,
    'depends': ['website_sale','payment','website'],
    'data': [
        'views/payment_view.xml',
        'views/payment_banesco_templates.xml',
        'data/payment_acquirer_data.xml',
        'views/templates.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_banesco/static/src/js/**/*',
        ],
    },
    'license': 'LGPL-3',
}
