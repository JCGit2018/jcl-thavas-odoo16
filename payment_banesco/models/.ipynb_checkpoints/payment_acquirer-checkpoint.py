# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('banesco', 'Banesco')], ondelete={'banesco': 'set default'})
    banesco_merchant_id = fields.Char(required_if_provider='banesco', string="Merchant id")
    banesco_access_key = fields.Char(required_if_provider='banesco', string="Access Key")
    banesco_secret_key = fields.Char(required_if_provider='banesco', string="Banesco Secret Key")
    banesco_profile_id = fields.Char(required_if_provider='banesco', string="Profile ID")
    banesco_url_test = fields.Char(required_if_provider='banesco', string="URL pruebas")
    banesco_url_prod = fields.Char(required_if_provider='banesco', string="URL produccion")

 
    
    @api.depends('provider')
    def _compute_view_configuration_fields(self):
        """ Override of payment to hide the credentials page.

        :return: None
        """
        super()._compute_view_configuration_fields()
        #self.filtered(lambda acq: acq.provider == 'banesco').show_credentials_page = True
        self.filtered(lambda acq: acq.provider == 'banesco').show_allow_tokenization = True

    
    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'banesco':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_banesco.payment_method_banesco').id

