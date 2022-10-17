# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

_logger = logging.getLogger(__name__)

from odoo import _, api, models,fields
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils






class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    
    banesco_transaction_id = fields.Char(string="Id transacción" )
    
    banesco_approval_code = fields.Char( string="Codigo aprobación")
    
    banesco_capture_code = fields.Char( string="Codigo captura")
    
    banesco_reversal_reason = fields.Char( string="Razón reverso")
    

    def _send_payment_request(self):
        """ Override of payment to simulate a payment request.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_payment_request()
        if self.provider != 'banesco':
            return

        # The payment request response would normally transit through the controller but in the end,
        # all that interests us is the reference. To avoid making a localhost request, we bypass the
        # controller and handle the fake feedback data directly.
        self._handle_feedback_data('banesco', {'reference': self.reference})
        
    def _send_capture_request(self):
        """ Override of payment to send a capture request to Banesco.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_capture_request()
        if self.provider != 'banesco':
            return
        
        raise ValidationError('Capture')
        
        #authorize_API = AuthorizeAPI(self.acquirer_id)
        #rounded_amount = round(self.amount, self.currency_id.decimal_places)
        #res_content = capture_payment(self.acquirer_reference)
        _logger.info("capture request response:\n%s", pprint.pformat(res_content))
        # As the API has no redirection flow, we always know the reference of the transaction.
        # Still, we prefer to simulate the matching of the transaction by crafting dummy feedback
        # data in order to go through the centralized `_handle_feedback_data` method.
        feedback_data = {'reference': self.reference, 'response': res_content}
        self._handle_feedback_data('banesco', feedback_data)

    def _send_void_request(self):
        """ Override of payment to send a void request to Authorize.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_void_request()
        if self.provider != 'banesco':
            return
        raise ValidationError('Void')
        authorize_API = AuthorizeAPI(self.acquirer_id)
        res_content = authorize_API.void(self.acquirer_reference)
        _logger.info("void request response:\n%s", pprint.pformat(res_content))
        # As the API has no redirection flow, we always know the reference of the transaction.
        # Still, we prefer to simulate the matching of the transaction by crafting dummy feedback
        # data in order to go through the centralized `_handle_feedback_data` method.
        feedback_data = {'reference': self.reference, 'response': res_content}
        self._handle_feedback_data('authorize', feedback_data)    

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        """ Override of payment to find the transaction based on dummy data.

        :param str provider: The provider of the acquirer that handled the transaction
        :param dict data: The dummy feedback data
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'banesco':
            return tx

        reference = data['req_reference_number']
        tx = self.search([('reference', '=', reference), ('provider', '=', 'banesco')])

        if not tx:
            raise ValidationError(
                "Banesco: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_feedback_data(self, data):
        """ Override of payment to process the transaction based on dummy data.

        Note: self.ensure_one()

        :param dict data: The dummy feedback data
        :return: None
        :raise: ValidationError if inconsistent data were received
        """

        if self.provider != "banesco":
            return
        #parametros = self.env['payment.acquirer'].sudo().search([('provider','=','banesco')])
        payment_state = data['decision']
        if payment_state =='ACCEPT':
            if self.acquirer_id.capture_manually:
                self._set_authorized()
                _logger.info("authorize request response:\n%s", pprint.pformat(data))
            else:
                self._set_done()  
                _logger.info("authorize and capture request response:\n%s", pprint.pformat(data))
            
            #se graba el id de la transaccion para eventual cptre en caso de authorizacion
            self.write({
                 'acquirer_reference': data['transaction_id']
            }
             )
                
        elif payment_state =='DECLINED':    
            self._set_canceled('Tu pago ha sido rechazado.') #cancelar transaccion  
            _logger.info("declined request response:\n%s", pprint.pformat(data))
        elif payment_state =='CANCEL':    
            self._set_canceled('La Transacción ha sido Cancelada') #cancelar transaccion  
            _logger.info("canelled request response:\n%s", pprint.pformat(data))
        elif payment_state =='REVIEW':    
            self._set_pending() #revisar transaccion  
            _logger.info("pending request response:\n%s", pprint.pformat(data))
        
        elif payment_state =='ERROR':
            self._set_error('Error Procesando el pago')
            _logger.info("error request response:\n%s", pprint.pformat(data))
        
        if self.tokenize:
            token = self.env['payment.token'].create({
                'acquirer_id': self.acquirer_id.id,
                'name': payment_utils.build_token_name(payment_details_short=data['req_card_number']),
                'partner_id': self.partner_id.id,
                'acquirer_ref': data['transaction_id'],
                'verified': True,
            })
            
            self.token_id = token.id
         