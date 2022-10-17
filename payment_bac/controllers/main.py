# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
import os
import json
from odoo.exceptions import UserError
from uuid import uuid4
from datetime import datetime, timezone
from base64 import b64encode, b64decode
from hashlib import sha256
import hashlib
import hmac
import logging
import pprint
import requests

_logger = logging.getLogger(__name__)


class PaymentBAC_Controller(http.Controller):
    
    @http.route('/payment/bac/authenticate', type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def index(self,**kw):

      data= json.loads(kw.get('response_content', -1))
      
      with open('/home/odoo/src/user/data_transac.txt', 'w') as temp_file:
                temp_file.write("%s\n" % data)

      token = self.request_token(**data)
      with open('/home/odoo/src/user/data_token.txt', 'w') as temp_file:
                temp_file.write("%s\n" % token)
                
      if not token:
        return request.redirect('/payment/status') 

      url_a_usar = 'https://staging.ptranz.com/api/spi/Conductor'

    
      return  http.request.render('payment_bac.authenticate',{
          'host_url': url_a_usar,
          'spi_token': token
      })
  
      
            
    def request_token(self,**data):
        
        #url = "https://staging.ptranz.com/api/spi/auth"
        
        host_url = request.httprequest.host_url
        return_url = host_url + 'payment/bac/return'
        
        with open('/home/odoo/src/user/data_proc.txt', 'w') as temp_file:
                temp_file.write("%s\n" % return_url)
        
        acquirer_id = data['acquirer_id']
        
        parametros = request.env['payment.acquirer'].sudo().search([('id','=', acquirer_id)])#revisar se confunde cuado instala otro acquirer???
        #parametros = request.env['payment.acquirer'].sudo().search([('provider','=', 'bac')])
        
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', data['reference'])]) 
        
        nombre = tx.partner_id.name.split(' ')[0]
        apellido = tx.partner_id.name.split(' ')[-1]


        if parametros.state=='test':
          url_base = parametros.bac_url_test
        elif parametros.state=='enabled':
          url_base = parametros.bac_url_prod
        
        if parametros.capture_manually:
            url = url_base + "/api/spi/auth" #combinar url test o prod con el endpoint 
        else:
            url =  url_base + "/api/spi/sale"
  
    
        orderTotalAmount = data['amount']
        moneda= request.env['res.currency'].sudo().search([('id','=', data['currency_id'])])
        
        #conversion a USD si la transaccion se hace en otra moneda
        if moneda.name !='USD':
             orderTotalAmount =  "{0:.2f}".format(moneda.inverse_rate * data['amount'])
      
        
        payload = json.dumps({
          "TransactionIdentifier": "",
          "TotalAmount": orderTotalAmount,
          "CurrencyCode": "840",
          "ThreeDSecure": True,
          "Source": {
            "CardPan": data['numTarjeta'],#"4012000000020071",
            "CardCvv": data['codigoTarjeta'],#"", 
            "CardExpiration": data['expiraAno'] + data['expiraMes'],#"2501",
            "CardholderName": data['nombreCliente'],#"John Doe",
          },
          "OrderIdentifier": data['reference'],
          '''  
          "BillingAddress": {
            "FirstName": nombre,
            "LastName": apellido,
            "Line1": tx.partner_id.street,
            "Line2": "", #ver campo odoo
            "City": tx.partner_id.city,
            "State": "MA",#tx.partner_id.state_id.name, #,ver si se puede poner codigo del estado
            "PostalCode": tx.partner_id.zip,
            "CountryCode": "840", #codigo iso para convertir desde el codigo odoo
            "EmailAddress": tx.partner_id.email,
            "PhoneNumber": tx.partner_id.phone
          },
          '''
          "AddressMatch": False,
          "ExtendedData": {
            "ThreeDSecure": {
              "ChallengeWindowSize": 4,
              "ChallengeIndicator": "01"
            },
            #usar funcion para url server
            "MerchantResponseUrl": return_url,
          }
          })
        headers = {
          'PowerTranz-PowerTranzId': parametros.bac_merchant_id,
          'PowerTranz-PowerTranzPassword': parametros.bac_password,
          'Content-Type': 'application/json'
        }

        with open('/home/odoo/src/user/respuesta_payload.txt', 'w') as temp_file:
                temp_file.write("%s\n" % payload)

        
        response = requests.request("POST", url, headers=headers, data=payload)

        respuesta= response.json()
        with open('/home/odoo/src/user/respuesta_paso1.txt', 'w') as temp_file:
               temp_file.write("%s\n" % respuesta)

        try:        
           token = respuesta['SpiToken']
           return token
        
        except:
            
            #raise UserError('Error al procesar su pago')
            request.env['payment.transaction'].sudo()._handle_feedback_data('bac', respuesta)
            return False
        
    _return_url = '/payment/bac/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def bac_return_from_redirect(self, **data):
        
        _logger.info("received notification data:\n%s", pprint.pformat(data))
        with open('/home/odoo/src/user/respuesta_host.txt', 'w') as temp_file:
                temp_file.write("%s\n" % data)
                
        url = "https://staging.ptranz.com/api/spi/payment"
        token = data['SpiToken']
        with open('/home/odoo/src/user/respuesta_token.txt', 'w') as temp_file:
                temp_file.write("%s\n" % token)

        request_id= data['TransactionIdentifier']
        payload = json.dumps(token)
        headers = {
          'Request-Id': request_id,
          'Host': 'staging.ptranz.com',
          'Accept': 'text/plain',
          'Content-Type': 'application/json-patch+json',
          'Content-Length': 'TBD'
        }
        

        response = requests.request("POST", url, headers=headers, data=payload)
        respuesta= response.json()
        with open('/home/odoo/src/user/respuesta_payment.txt', 'w') as temp_file:
                temp_file.write("%s\n" % respuesta)
        
                
        request.env['payment.transaction'].sudo()._handle_feedback_data('bac', respuesta)
    
        return request.redirect('/payment/status')        

            
