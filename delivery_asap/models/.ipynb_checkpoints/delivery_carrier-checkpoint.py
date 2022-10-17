# -*- coding: utf-8 -*-


'''
Se crea la opcion ASAP como proveedor de mensajeria

'''

from odoo import models, fields, api, _
import requests
from odoo.exceptions import UserError, RedirectWarning
import json
from odoo.osv import expression


class Delivery_Asap(models.Model):
    _inherit = 'delivery.carrier'
    
    '''
    _api_key = '6CHfxdW4Cot9JUC8Tpqk39ii9dNjJwNDobXsLECwNxxxg3GzJDqAZH'
    _token= "de35f2afca72da9aa566224eafcef6cf0a60e313"
    _shared_secret = "8a393bed8a62e2f349ca47e33f5286fa353adab3"
    
    _headers = {
        'x-api-key': _api_key,
        'Content-Type': 'application/json'
        }

    
    _url_test = "https://goasap.dev/ecommerce/v2/api/order"
    _url_prod = "https://goasap.app/ecommerce/v2/api/order"
    '''
    #campos para conexion a ASAP
    asap_api_key = fields.Char(string='Key') 
    asap_token= fields.Char(string='Token') 
    asap_shared_secret = fields.Char(string='Secret') 
    asap_url_test = fields.Char(string='URL Pruebas') 
    asap_url_prod = fields.Char(string='URL Producción') 
    asap_price = fields.Float(string='Costo Envío')
    

    
    #delivery_log= fields.Selection([('0','Sin log'), ('1','Con log')], string='Id del envío')
    #reason = fields.Char()
    #deben ir en configuracion


    #crear con para verifcar stus de las ordenes  informar por mensaje o sms o listado o cambio en status del picking
    
    delivery_type = fields.Selection(selection_add=[
        ('asap', "ASAP")
    ], ondelete={'asap': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})})
    
    
    def asap_rate_shipment(self,order):
         ''' Funcion para calculo de costos de envio en el carrito de compras
          
         Parametros:
        
         order : Objeto coorespondiente a la orden de entrega, proviene del web site
         retorna el precio del envío
         '''
        
         #calculo de costos de envio
         price = self.asap_price
         return {'success': True,
                'price': price,
                'error_message': False,
                'warning_message': False}
        
        
        
    def asap_send_shipping(self, pickings):
        ''' Crea el envío en ASAP
        
         Parametros:
         pickings: entregas a incluir en el envio
         retorna los datos de envío : precio y número de envío
        '''
        
        # si esta en prueba o produccion
        if self.prod_environment:
            url_a_usar =  self.asap_url_prod
        else:
            url_a_usar = self.asap_url_test
            
        headers = {
        'x-api-key':self.asap_api_key,
        'Content-Type': 'application/json'
        }

        if not url_a_usar:
            
            raise UserError(_('Recuerde configurar los URL en el metodo de envío'))
            
        url = f"{url_a_usar}/order"    

        #crea la orden
        res = []
        data_envio = dict()
        
        data_envio["user_token"] = self.asap_token
        
        data_envio["shared_secret"] = self.asap_shared_secret
        
        
        for picking in pickings:
            data_envio["type_id"] = 2 #picking.type_id siempre va a ser shopping
            data_envio["is_personal"] = 0 #picking.personalsiempre va aser bussiness
            data_envio["is_oneway"] =  1 if not picking.is_return_picking else 0
            
            data_envio["source_address"] = picking.company_id.partner_id.contact_address_complete
            if self.prod_environment:
                data_envio["phone"] = picking.company_id.partner_id.phone
            #data_envio["source_lat"] = picking.company_id.partner_id.partner_latitude
            data_envio["source_lat"] = 8.9853921
            #data_envio["source_long"] = picking.company_id.partner_id.partner_longitude
            data_envio["source_long"] = -79.5131792
            data_envio["special_inst"] = picking.special_inst or "Instrucciones"
            
            data_envio["desti_address"] = picking.partner_id.contact_address_complete
            #data_envio["desti_lat"] = picking.partner_id.partner_latitude
            #data_envio["desti_long"] = picking.partner_id.partner_longitude
            data_envio["desti_lat"] = 9.0218638
            data_envio["desti_long"] = -79.4650207

            data_envio["dest_special_inst"] = picking.dest_special_inst or 'Instrucciones'
            data_envio["vehicle_type"] = picking.vehicle_type or 'bike'
            data_envio["request_later"]= picking.request_later or 0
            if picking.request_later == '1':
               data_envio["request_later_time"] =  picking.request_later_time
                       
        payload = json.dumps(data_envio)
        try: 
          response = requests.request("POST", url, headers= headers, data=payload)
          response = response.json()
          picking.carrier_tracking_ref= response['result']['delivery_id']
          picking.message_post(body=_(f'El envío #{picking.carrier_tracking_ref} ha sido creado'))
        except Exception as e:
            raise UserError('No es posible crear el pedido')

        #carrier_tracking_ref se genera luego del envio
        shipping_data = {
                'exact_price': self.asap_price,
                'tracking_number': picking.carrier_tracking_ref}
        
        res = res + [shipping_data]
       
        
        return res
        
    def asap_get_tracking_link(self,picking):
        
        #picking.carrier_tracking_ref id del envio en el caso de asap
        #hacer la consulta para regreasr el link de tracking
        
        headers = {
        'x-api-key':self.asap_api_key,
        'Content-Type': 'application/json'
        }
        
        if self.prod_environment:
            url_a_usar =  self.asap_url_prod
        else:
            url_a_usar = self.asap_url_test

        if not url_a_usar:
            
            raise UserError(_('Recuerde configurar los URL en el metodo de envío'))

        #url_a_usar = "https://goasap.dev/ecommerce/v2/api/order"
        delivery_id = picking.carrier_tracking_ref
        
        url = f"{url_a_usar}/order/tracking?user_token={self.asap_token}&shared_secret={self.asap_shared_secret}&delivery_id={delivery_id}"
        
        payload={}

        response = requests.request("GET", url, headers= headers, data=payload)        
        
        
        response_body = response.json()
        try:
            if response_body['status']:
                return response_body['tracking_link']
        except:
          raise UserError(_('Por los momentos no es posible generar el Tracking'))
    
    def asap_cancel_shipment(self, picking):
      
        if self.prod_environment:
            url_a_usar =  self.asap_url_prod
        else:
            url_a_usar = self.asap_url_test

        
        
        url = f"{url_a_usar}/cancel"
        
        headers = {
        'x-api-key':self.asap_api_key,
        'Content-Type': 'application/json'
        }

        
        payload = json.dumps({
             "user_token": self.asap_token,
             "shared_secret": self.asap_shared_secret,
             "delivery_id": picking.carrier_tracking_ref,
             "addn_reason": 'Cancelación de orden'
             })
       
        #response = requests.request("POST", url, headers = headers, data=payload)

        #response_body = response.json()

    
        try:
            response = requests.request("POST", url, headers = headers, data=payload)

            response_body = response.json()
            
            if response_body['flag']:
               picking.message_post(body=_(f'El envio #{picking.carrier_tracking_ref} ha sido cancelado'))
               picking.write({'carrier_tracking_ref': '',
                           'carrier_price': 0.0})
        except:
            raise UserError(_('No es posible cancelar el envío en estos momentos'))
        
    
    def asap_default_custom_package_code(self):
        pass

    
    def _ultimo_estatus_orden(self, picking, carrier_id):
        
          carrier =self.search([('id','=',carrier_id)])
          headers = {
            'x-api-key':carrier.asap_api_key,
            'Content-Type': 'application/json'
          }

            
          delivery_id = picking 
          
          if self.prod_environment:
              url_a_usar =  carrier.asap_url_prod
          else:
              url_a_usar = carrier.asap_url_test
                
          
          if not url_a_usar:
            
            raise UserError(_('Recuerde configurar los URL en el metodo de envío'))
          
          #url_a_usar = 'https://goasap.dev/ecommerce/v2/api'  
        
          url = f"{url_a_usar}/order/status?token={carrier.asap_token}&delivery_id={delivery_id}&shared_secret={carrier.asap_shared_secret}"
          
          #url = "https://goasap.dev/ecommerce/v2/api/order/status?token=de35f2afca72da9aa566224eafcef6cf0a60e313&delivery_id=14923&shared_secret=8a393bed8a62e2f349ca47e33f5286fa353adab3"
         
        
          payload={}

          #response = requests.request("GET", url, self._headers, data=payload)
          try:
            
              response = requests.request("GET", url, headers = headers, data=payload)  
            
              response = response.json()  
   
              return response['delivery_status']
              
          except:
              raise UserError(_('No es posible obtner el eststus del pedido en estos momentos'))
        
          '''
          Respuesta
          {
    "status": true, 
    "delivery_status": 0,
    "provider_status": 0,
    "status_message": "Order Placed",
    "updated_at": "2022-04-30T17:07:41.000Z"
}
          
          '''        


    def _historico_status_orden(self, picking, carrier_id):
         
         carrier =self.search([('id','=',carrier_id)])
         headers = {
            'x-api-key':carrier.asap_api_key,
            'Content-Type': 'application/json'
          }

            
         delivery_id = picking 
          
         if self.prod_environment:
              url_a_usar =  carrier.asap_url_prod
         else:
              url_a_usar = carrier.asap_url_test
                
          
         if not url_a_usar:
            
            raise UserError(_('Recuerde configurar los URL en el metodo de envío'))

        
         #url_a_usar = 'https://goasap.dev/ecommerce/v2/api' 
        
         #url = "https://goasap.dev/ecommerce/v2/api/order/log?delivery_id=14923&token=de35f2afca72da9aa566224eafcef6cf0a60e313&delivery_log=1&shared_secret=8a393bed8a62e2f349ca47e33f5286fa353adab3"
         
         url = f"{url_a_usar}/order/log?delivery_id={delivery_id}&token={carrier.asap_token}&delivery_log=1&shared_secret={carrier.asap_shared_secret}"
         
         payload={}
         
         
            
         #esponse = requests.request("GET", url, headers= headers, data=payload)
         #rint(response.json())
         my_dict = {       
          "status": True,
          "delivery_log": [
           {
            "id": 59826,
            "delivery_status": 0,
            "provider_status": 0,
            "description": "Order Status updated to CONFIRMING_ORDER",
            "logged_at": "2022-04-30T17:07:43.000Z"
          }
         ],
          "provider_log": [
           {
            "id": 59826,
            "provider_status": 0,
            "logged_at": "2022-04-30T17:07:43.000Z"
           }
         ]
         }
         
         result=''
         result= result + 'Log del envío\n'
         list_delivery = my_dict['delivery_log']
         for item in list_delivery:
             id = item['id']
             estado = item['delivery_status']
             registro = item['logged_at']
             descripcion = item['description']
             proveedor = item['provider_status']
             result= result + f'ID: {id:7} Hora: {registro:25} Estado del envio: {estado:8} Estado proveedor: {proveedor:8} Descripción: {descripcion:8}\n'   
         result= result + '\n'
         result= result +'Log del proveedor\n'
         list_provider = my_dict['provider_log']
         for item in list_provider:
             id = item['id']
             registro = item['logged_at']
             proveedor = item['provider_status']
             result= result + f'ID: {id:7} Hora: {registro:25} Estado proveedor: {proveedor:8}\n'
         #raise UserError(result)
         raise RedirectWarning('Transfers %s: Please add some items to move.' % ',' 'hola')

         '''
         en caso de error
         {
          "message": "No such id exists.",
          "status": false
         }
         '''   

