# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('bac', 'BAC CREDOMATIC')], ondelete={'bac': 'set default'})
    bac_merchant_id = fields.Char(required_if_provider='bac', string="Merchant id")
    bac_password = fields.Char(required_if_provider='bac', string="Password")
    bac_url_test = fields.Char(required_if_provider='bac', string="URL pruebas")
    bac_url_prod = fields.Char(required_if_provider='bac', string="URL produccion")

 
    
    @api.depends('provider')
    def _compute_view_configuration_fields(self):
        """ Override of payment to hide the credentials page.

        :return: None
        """
        super()._compute_view_configuration_fields()
        self.filtered(lambda acq: acq.provider == 'bac').show_allow_tokenization = True

    
    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'bac':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_bac.payment_method_bac').id

