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

_logger = logging.getLogger(__name__)

def create_sha256_signature(key, message):
    """
    Signs an HMAC SHA-256 signature to a message with Base 64
    encoding. This is required by CyberSource.
    """
    
    digest = hmac.new(
        key.encode(),
        msg=message.encode(),
        digestmod=sha256,
    ).digest()
    return b64encode(digest).decode()


def sign_fields_to_context(fields, context, secret_key):
    """
    Builds the list of file names and data to sign, and created the
    signature required by CyberSource.
    """
    
    
    
    signed_field_names = []
    data_to_sign = []
    for key, value in fields.items():
        signed_field_names.append(key)
    # Build the fields into a list to sign, which will become
    # a string when joined by a comma
    for key, value in fields.items():
        data_to_sign.append(f'{key}={value}')
    
    #print(data_to_sign)
    
    context['fields'] = fields
    context['signature'] = create_sha256_signature(
        secret_key,
        ','.join(data_to_sign)
    )
    

    return context

def generate_signature(key,**data):
    #print(data)
    #print(key)
    context = dict()
    to_send = sign_fields_to_context(data,context,key)
    return to_send['signature']



class PaymentBanescoController(http.Controller):
    
    @http.route('/payment/banesco/authenticate', type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def index(self,**kw):
      data= json.loads(kw.get('response_content', -1))
      
      
      acquirer_id = data['acquirer_id']
        
      tx = request.env['payment.transaction'].sudo().search([('reference', '=', data['reference'])])  
        
      parametros = request.env['payment.acquirer'].sudo().search([('id','=', acquirer_id)])

      if parametros.state=='test':
          url_a_usar = parametros.banesco_url_test
      elif parametros.state=='enabled':
          url_a_usar = parametros.banesco_url_prod
  
      secret_key =  parametros.banesco_secret_key
     
      orderTotalAmount = data['amount']
       
      moneda= request.env['res.currency'].sudo().search([('id','=', data['currency_id'])])
        
        #convesrion a USD si la transaccion se hace en otra moneda
      if moneda.name !='USD':
         orderTotalAmount =  "{0:.2f}".format(moneda.inverse_rate * data['amount'])
      
      if parametros.capture_manually:
          transaction = 'authorization'
      else:
          transaction = 'sale' 
            
      transaction_uuid = uuid4().hex   
      my_time= datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
      nombre = tx.partner_id.name.split(' ')[0]
      apellido = tx.partner_id.name.split(' ')[-1]

      envio = tx.sale_order_ids.partner_shipping_id #datos de envio
      nombre_envio = envio.name.split(' ')[0]
      apellido_envio = envio.name.split(' ')[-1]
    
      #url de retorno y cancelacion
      host_url = request.httprequest.host_url
      return_url = host_url + 'payment/banesco/return'

    
      #telefono facturacion
      if not tx.partner_id.phone:
        telefono = '' 
      else:  
        telefono = tx.partner_id.phone   
      
      payload= {
            'access_key': parametros.banesco_access_key, #tomar del modelo
            'profile_id': parametros.banesco_profile_id,
            'transaction_uuid': transaction_uuid,
            'signed_field_names': 'access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,merchant_defined_data1,merchant_defined_data2,merchant_defined_data3,merchant_defined_data4,merchant_defined_data5,merchant_defined_data6,merchant_defined_data7,merchant_defined_data8,merchant_defined_data10,merchant_defined_data24,merchant_defined_data28,bill_to_forename,bill_to_surname,bill_to_email,bill_to_address_line1,bill_to_address_city,bill_to_address_postal_code,bill_to_address_state,bill_to_address_country,bill_to_phone,ship_to_forename,ship_to_surname,ship_to_email,ship_to_address_line1,ship_to_address_city,ship_to_address_postal_code,ship_to_address_state,ship_to_address_country,ship_to_phone,override_custom_cancel_page,override_custom_receipt_page',
            'unsigned_field_names':'',
            'signed_date_time': my_time,         
            'locale': 'es-mx',
            'transaction_type': transaction, #se escoge por el check de captura manual
            'reference_number': data['reference'],
            'amount': orderTotalAmount,
            'currency': 'USD',
            "merchant_defined_data1": parametros.banesco_merchant_id.upper(),
            "merchant_defined_data2": 'WEB',
            "merchant_defined_data3": data['reference'].upper(), #referencia de venta
            "merchant_defined_data4": 'RETAIL',
            "merchant_defined_data5": tx.company_id.name.upper(),#nombre del comercio
            "merchant_defined_data6": "CATEGORY1", #categoria de productos
            "merchant_defined_data7": tx.partner_id.email.upper() or tx.partner_id.name.upper(), #datos del cliente 
            "merchant_defined_data8": "NO", #Compra a tercero
            "merchant_defined_data10": "YES", #Email was confirmed
            "merchant_defined_data24": "NO",#TOKENIZATION
            "merchant_defined_data28": "001", #sucursal,
            "bill_to_forename":nombre,
            "bill_to_surname":apellido,
            'bill_to_email':tx.partner_id.email if tx.partner_id.email else '' ,
            'bill_to_address_line1':tx.partner_id.street if  tx.partner_id.street else '',
            'bill_to_address_city':tx.partner_id.city if tx.partner_id.city else '' ,
            'bill_to_address_postal_code':tx.partner_id.zip if tx.partner_id.zip else'',
            'bill_to_address_state': tx.partner_id.state_id.code if tx.partner_id.state_id.code else '', 
            'bill_to_address_country':tx.partner_id.country_id.code if tx.partner_id.country_id.code else '',
            'bill_to_phone': telefono,
            "ship_to_forename":nombre_envio if nombre_envio else '' ,
            "ship_to_surname":apellido_envio if apellido_envio else '',
            'ship_to_email':envio.email if envio.email else '' ,
            'ship_to_address_line1':envio.street if envio.street else '',
            'ship_to_address_city':envio.city if envio.city else '',
            'ship_to_address_postal_code':envio.zip if envio.zip else '',
            'ship_to_address_state': envio.state_id.code if envio.state_id.code else '',
            'ship_to_address_country':envio.country_id.code,
            'ship_to_phone': envio.phone if envio.phone else '',
            'override_custom_cancel_page': return_url,
            'override_custom_receipt_page': return_url
          
      }

      _logger.info("datos envio:\n%s", pprint.pformat(payload))
     
      my_signature = generate_signature(secret_key,**payload)
      
      return http.request.render('payment_banesco.authenticate', {
            'host_url': url_a_usar,
            'access_key': parametros.banesco_access_key,
            'profile_id': parametros.banesco_profile_id,
            'transaction_uuid': transaction_uuid,
            'signed_field_names': 'access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,merchant_defined_data1,merchant_defined_data2,merchant_defined_data3,merchant_defined_data4,merchant_defined_data5,merchant_defined_data6,merchant_defined_data7,merchant_defined_data8,merchant_defined_data10,merchant_defined_data24,merchant_defined_data28,bill_to_forename,bill_to_surname,bill_to_email,bill_to_address_line1,bill_to_address_city,bill_to_address_postal_code,bill_to_address_state,bill_to_address_country,bill_to_phone,ship_to_forename,ship_to_surname,ship_to_email,ship_to_address_line1,ship_to_address_city,ship_to_address_postal_code,ship_to_address_state,ship_to_address_country,ship_to_phone,override_custom_cancel_page,override_custom_receipt_page',
            'unsigned_field_names':'',
            'signed_date_time': my_time,         
            'locale': 'es-mx',
            'transaction_type': transaction, #se escoge por el check de captura amnual
            'reference_number': data['reference'],
            'amount': orderTotalAmount,
            'currency': 'USD',
            "bill_to_forename":nombre if nombre else '',
            "bill_to_surname":apellido if apellido else '',
            'bill_to_email':tx.partner_id.email if tx.partner_id.email else '' ,
            'bill_to_address_line1':tx.partner_id.street if tx.partner_id.street else '',
            'bill_to_address_city':tx.partner_id.city if  tx.partner_id.city else '',
            'bill_to_address_postal_code':tx.partner_id.zip if tx.partner_id.zip else '',
            'bill_to_address_state': tx.partner_id.state_id.code if tx.partner_id.state_id.code else '', 
            'bill_to_address_country':tx.partner_id.country_id.code if tx.partner_id.country_id.code else '' ,
            'bill_to_phone': telefono,
            "ship_to_forename":nombre_envio if nombre_envio else '',
            "ship_to_surname":apellido_envio if apellido_envio else '',
            'ship_to_email':envio.email if envio.email else '',
            'ship_to_address_line1':envio.street if envio.street else '',
            'ship_to_address_city':envio.city if envio.city else '',
            'ship_to_address_postal_code':envio.zip if envio.zip else '',
            'ship_to_address_state': envio.state_id.code if envio.state_id.code else '',
            'ship_to_address_country':envio.country_id.code,
            'ship_to_phone': envio.phone if envio.phone else '',
            "merchant_defined_data1": parametros.banesco_merchant_id.upper(),
            "merchant_defined_data2": 'WEB',
            "merchant_defined_data3": data['reference'].upper(), #referencia de venta
            "merchant_defined_data4": 'RETAIL',
            "merchant_defined_data5": tx.company_id.name.upper(),#nombre del comercio
            "merchant_defined_data6": "CATEGORY1", #categoria de productos
            "merchant_defined_data7": tx.partner_id.email.upper() or tx.partner_id.name.upper(), #datos del cliente 
            "merchant_defined_data8": "NO", #Compra a tercero
            "merchant_defined_data10": "YES", #Email was confirmed
            "merchant_defined_data24": "NO",#TOKENIZATION
            "merchant_defined_data28": "001", #sucursal
            'override_custom_cancel_page': return_url,
            'override_custom_receipt_page': return_url,
            'signature':my_signature
      })

#override_backoffice_post_url no creo que se use
#override_custom_cancel_page
#override_custom_receipt_page
        
    _return_url = '/payment/banesco/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def banesco_return_from_redirect(self, **data):
        
        _logger.info("received notification data:\n%s", pprint.pformat(data))
        
        request.env['payment.transaction'].sudo()._handle_feedback_data('banesco', data)
    
        return request.redirect('/payment/status')        

            
