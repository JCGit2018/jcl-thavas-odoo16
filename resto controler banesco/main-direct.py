# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
from CyberSource import *
import os
import json
from importlib.machinery import SourceFileLoader
from odoo.exceptions import UserError
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing



#config_file = os.path.join(os.getcwd(), "Configuration.py")
config_file =  "src/user/payment_banesco/controllers/Configuration.py"
configuration = SourceFileLoader("module.name", config_file).load_module()

class PaymentPostProcessingInherit(PaymentPostProcessing):
    @http.route('/payment/status', type='http', auth='public', website=True, sitemap=False)
    def display_status(self, **kwargs):
        """ Display the payment status page.

        :param dict kwargs: Optional data. This parameter is not used here
        :return: The rendered status page
        :rtype: str
        """

        res = super(PaymentPostProcessingInherit, self).display_status(**kwargs)
        return 'hello'
        #return res
        



class PaymentBanescoController(http.Controller):
    
    #parte 1 autenticacion
    @http.route('/payment/banesco/authenticate', type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def index(self,**kw):
      data= json.loads(kw.get('response_content', -1))
      
      respuesta = self.authenticate_card(**data)
        
        
      #reference_id =  response_content.reference_id  #pasar al paso 2
      
      with open('/home/odoo/src/user/respuesta_setup.txt', 'w') as temp_file:
                temp_file.write("%s\n" % respuesta.reference_id)

            
       
      return http.request.render('payment_banesco.authenticate', {
            'origin_url':"https://centinelapistag.cardinalcommerce.com", #hay que cambiarlo en prod
            'device_data_collection_url': respuesta.device_data_collection_url,
            'access_token': respuesta.access_token
      })

        
      #return request.redirect('/payment/status')
        
      def del_none(self,d):
        for key, value in list(d.items()):
            if value is None:
                del d[key]
            elif isinstance(value, dict):
                self.del_none(value)
        return d

      def authenticate_card(self,**data):
        
        
        acquirer_id = data['acquirer_id']
        
        parametros = request.env['payment.acquirer'].sudo().search([('id','=', acquirer_id)])

        tx = request.env['payment.transaction'].sudo().search([('reference', '=', data['reference'])])


        clientReferenceInformationCode = data['codCliente']
        clientReferenceInformationPartnerDeveloperId = "7891234"
        clientReferenceInformationPartnerSolutionId = "89012345"
        clientReferenceInformationPartner = Riskv1decisionsClientReferenceInformationPartner(
            developer_id = clientReferenceInformationPartnerDeveloperId,
            solution_id = clientReferenceInformationPartnerSolutionId
        )

        clientReferenceInformation = Riskv1decisionsClientReferenceInformation(
            code = clientReferenceInformationCode,
            partner = clientReferenceInformationPartner.__dict__
        )

        paymentInformationCardType = "001" #hay que traerlo de odoo con un select
        paymentInformationCardExpirationMonth = data['expiraMes']
        paymentInformationCardExpirationYear = data['expiraAno']
        paymentInformationCardNumber = data['numTarjeta']
        paymentInformationCard = Riskv1authenticationsetupsPaymentInformationCard(
            type = paymentInformationCardType,
            expiration_month = paymentInformationCardExpirationMonth,
            expiration_year = paymentInformationCardExpirationYear,
            number = paymentInformationCardNumber
        )

        paymentInformation = Riskv1authenticationsetupsPaymentInformation(
            card = paymentInformationCard.__dict__
        )

        requestObj = PayerAuthSetupRequest(
            client_reference_information = clientReferenceInformation.__dict__,
            payment_information = paymentInformation.__dict__
        )


        requestObj = self.del_none(requestObj.__dict__)
        requestObj = json.dumps(requestObj)


        try:
            config_obj = configuration.Configuration()
            client_config = config_obj.get_configuration()
            if parametros.state=='test':
               client_config["run_environment"] = parametros.banesco_url_test
            elif parametros.state=='enabled':
               client_config["run_environment"] = parametros.banesco_url_prod
            client_config['merchantid'] = parametros.banesco_merchant_id
            client_config['merchant_keyid'] = parametros.banesco_key
            client_config['merchant_secretkey'] = parametros.banesco_secret_key

            api_instance = PayerAuthenticationApi(client_config)
            return_data, status, body = api_instance.payer_auth_setup(requestObj)
            with open('/home/odoo/src/user/envio_setup.txt', 'w') as temp_file:
                temp_file.write("%s\n" % requestObj)
            
            with open('/home/odoo/src/user/setup_data.txt', 'w') as temp_file:
                temp_file.write("%s\n" % return_data)
            
            return return_data.consumer_authentication_information

        except Exception as e:
            #print("\nException when calling PayerAuthenticationApi->payer_auth_setup: %s\n" % e)
            with open('/home/odoo/src/user/error_setup.txt', 'w') as temp_file:
                temp_file.write("%s\n" % e)

            raise UserError(_(paymentInformationCardNumber + "\nException when calling PayerAuthenticationApi->payer_auth_setup: %s\n" % e))

            
    #json controller
    @http.route('/payment/banesco/payment', type='json', auth='public')
    def banesco_payment(self, **kwargs):
        #return request.redirect('/payment/banesco/authenticate')
        
        #realizar procesamientos para obtener datos del cliente y moneda, admeas de valores en blanco
        post = kwargs['processingValues']
        
        #response_content = self.authenticate_card(**post)

        #return request.redirect('/payment/banesco/status')
        return 
        
        feedback_data_banesco = {'reference': post['reference'], 'response': response_content}
        request.env['payment.transaction'].sudo()._handle_feedback_data('banesco', feedback_data_banesco)

        
    def del_none(self,d):
        for key, value in list(d.items()):
            if value is None:
                del d[key]
            elif isinstance(value, dict):
                self.del_none(value)
        return d

    def simple_authorizationinternet(self,flag,**data):
        
        acquirer_id = data['acquirer_id']
        
        parametros = request.env['payment.acquirer'].sudo().search([('id','=', acquirer_id)])

        tx = request.env['payment.transaction'].sudo().search([('reference', '=', data['reference'])])
        
        
        clientReferenceInformationCode = data['codCliente'] #ver que se pone ruc o...
        clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
            code = clientReferenceInformationCode
        )

        processingInformationCapture =  not parametros.capture_manually
            
        device_ip_address =  request.httprequest.environ['REMOTE_ADDR']  or '' 
        
        merchantDefinedInformation=[]
        
        merchantDefinedInformationvalues= {
            "1": parametros.banesco_merchant_id,
            "2": 'WEB',
            "3": data['reference'], #referencia de venta
            "4": 'RETAIL',
            "5": tx.company_id.name,#nombre del comercio
            "6": "CATEGORY1", #categoria de productos
            "7": tx.partner_id.email or tx.partner_id.name, #datos del cliente 
            "8": "NO", #Compra a tercero
            "10": "YES", #Email was confirmed
            "15": "Windows 10 64-bit",#Sistema Operativo utilizado en la orden
            "19": "1600811150",#fecha de la transac (timestamp)???
            "17": "9NKKSEV7",#Codigo de Autorizacion
            "21": "148",#numero factura
            "24": "NO",#TOKENIZATION
            "28": "001" #sucursal
            #MDD27	cantidad de productos
            
        }
        
        
        for _key,_value in merchantDefinedInformationvalues.items():
            merchantDefinedInformation1 = Ptsv2paymentsMerchantDefinedInformation(
             key = _key,
             value = _value
            )

            merchantDefinedInformation.append(merchantDefinedInformation1.__dict__)
        

        deviceInformation = Ptsv2paymentsDeviceInformation(
            ip_address = device_ip_address,
            fingerprint_session_id='123456789'
        )    
            
        processingInformation = Ptsv2paymentsProcessingInformation(
            capture = processingInformationCapture
        )

        paymentInformationCardNumber = data['numTarjeta']
        paymentInformationCardExpirationMonth = data['expiraMes'] 
        paymentInformationCardExpirationYear = data['expiraAno'] #"2031" año completo
        paymentInformationCardSecurityCode = data['codigoTarjeta']
        paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
            number = paymentInformationCardNumber,
            expiration_month = paymentInformationCardExpirationMonth,
            expiration_year = paymentInformationCardExpirationYear,
            security_code = paymentInformationCardSecurityCode
        )

        paymentInformation = Ptsv2paymentsPaymentInformation(
            card = paymentInformationCard.__dict__
        )

        
        orderInformationAmountDetailsTotalAmount = data['amount']
        
        
        moneda= request.env['res.currency'].sudo().search([('id','=', data['currency_id'])])
        
        #convesrion a USD si la transaccion se hace en otra moneda
        if moneda.name !='USD':
            orderInformationAmountDetailsTotalAmount =  "{0:.2f}".format(moneda.inverse_rate * data['amount'])
        
                
        orderInformationAmountDetailsCurrency = 'USD'
        orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
            total_amount = orderInformationAmountDetailsTotalAmount,
            currency = orderInformationAmountDetailsCurrency
        )
        
        
        #usar dummy de acuerdo a las indicaciones
        if data['nombreCliente']=='' or data['apellidoCliente']=='':
           orderInformationBillToFirstName = 'NoReal' #dato dummy
           orderInformationBillToLastName =  'Name'   #dato dummy
        else:    
           orderInformationBillToFirstName = data['nombreCliente']#tx.partner_id.name ver si se puede usar el uitls de split 
           orderInformationBillToLastName =  data['apellidoCliente']
            
            
        #datos dummy direccion, hay que ponerlos todos si falta alguno
        #orderInformationBillToAddress1 = '1295 Charleston Road'
        #orderInformationBillToLocality = 'Mountain View'
        #orderInformationBillToAdministrativeArea = 'CA'
        #orderInformationBillToPostalCode = '94043'
        #orderInformationBillToCountry = 'US'
        
        pais_a_buscar = data['paisCliente'].capitalize()
        pais= request.env['res.country'].sudo().search([('name','=', pais_a_buscar)])
        email = False
        if '@' in data['emailCliente']:
          email= data['emailCliente']   
        
        orderInformationBillToAddress1 = data['calle'] or tx.partner_id.street
        orderInformationBillToLocality = data['ciudadCliente'] or tx.partner_id.city
        orderInformationBillToAdministrativeArea = data['estadoCliente'] or tx.partner_id.state_id.name #si da error pirmers dos letras en uppercase
        orderInformationBillToPostalCode = data['codPostalCliente'] or tx.partner_id.zip
        orderInformationBillToCountry = pais.code or tx.partner_id.country_id.code
        orderInformationBillToEmail = email or tx.partner_id.email or 'null@cybersource.com'
        orderInformationBillToPhoneNumber = data['telCliente'] or tx.partner_id.phone
              
        orderInformationBillTo = Ptsv2paymentsOrderInformationBillTo(
            first_name = orderInformationBillToFirstName,
            last_name = orderInformationBillToLastName,
            address1 = orderInformationBillToAddress1,
            locality = orderInformationBillToLocality,
            administrative_area = orderInformationBillToAdministrativeArea,
            postal_code = orderInformationBillToPostalCode,
            country = orderInformationBillToCountry,
            email = orderInformationBillToEmail,
            phone_number = orderInformationBillToPhoneNumber
            
        )

        orderInformation = Ptsv2paymentsOrderInformation(
            amount_details = orderInformationAmountDetails.__dict__,
            bill_to = orderInformationBillTo.__dict__
        )

        requestObj = CreatePaymentRequest(
            client_reference_information = clientReferenceInformation.__dict__,
            processing_information = processingInformation.__dict__,
            payment_information = paymentInformation.__dict__,
            order_information = orderInformation.__dict__,
            device_information = deviceInformation.__dict__,
            merchant_defined_information = merchantDefinedInformation
        )


        requestObj = self.del_none(requestObj.__dict__)
        requestObj = json.dumps(requestObj)
        

        try:
            config_obj = configuration.Configuration()
            client_config = config_obj.get_configuration()
            if parametros.state=='test':
               client_config["run_environment"] = parametros.banesco_url_test
            elif parametros.state=='enabled':
               client_config["run_environment"] = parametros.banesco_url_prod
            client_config['merchantid'] = parametros.banesco_merchant_id
            client_config['merchant_keyid'] = parametros.banesco_key
            client_config['merchant_secretkey'] = parametros.banesco_secret_key

            
            api_instance = PaymentsApi(client_config)
            return_data, status, body = api_instance.create_payment(requestObj)

            with open('/home/odoo/src/user/body_respuesta.txt', 'w') as temp_file:
                temp_file.write("%s\n" % body)
            with open('/home/odoo/src/user/status_respuesta.txt', 'w') as temp_file:
                temp_file.write("%s\n" % status)
                
            return return_data
        
        except Exception as e:
            raise UserError(_('En estos momentos No se puede procesar su pago ' +"%s\n" % e))
    

  
        
    def authenticate_card(self,**data):
        
        
        acquirer_id = data['acquirer_id']
        
        parametros = request.env['payment.acquirer'].sudo().search([('id','=', acquirer_id)])

        tx = request.env['payment.transaction'].sudo().search([('reference', '=', data['reference'])])


        clientReferenceInformationCode = data['codCliente']
        clientReferenceInformationPartnerDeveloperId = "7891234"
        clientReferenceInformationPartnerSolutionId = "89012345"
        clientReferenceInformationPartner = Riskv1decisionsClientReferenceInformationPartner(
            developer_id = clientReferenceInformationPartnerDeveloperId,
            solution_id = clientReferenceInformationPartnerSolutionId
        )

        clientReferenceInformation = Riskv1decisionsClientReferenceInformation(
            code = clientReferenceInformationCode,
            partner = clientReferenceInformationPartner.__dict__
        )

        paymentInformationCardType = "001" #hay que traerlo de odoo con un select
        paymentInformationCardExpirationMonth = data['expiraMes']
        paymentInformationCardExpirationYear = data['expiraAno']
        paymentInformationCardNumber = data['numTarjeta']
        paymentInformationCard = Riskv1authenticationsetupsPaymentInformationCard(
            type = paymentInformationCardType,
            expiration_month = paymentInformationCardExpirationMonth,
            expiration_year = paymentInformationCardExpirationYear,
            number = paymentInformationCardNumber
        )

        paymentInformation = Riskv1authenticationsetupsPaymentInformation(
            card = paymentInformationCard.__dict__
        )

        requestObj = PayerAuthSetupRequest(
            client_reference_information = clientReferenceInformation.__dict__,
            payment_information = paymentInformation.__dict__
        )


        requestObj = self.del_none(requestObj.__dict__)
        requestObj = json.dumps(requestObj)


        try:
            config_obj = configuration.Configuration()
            client_config = config_obj.get_configuration()
            if parametros.state=='test':
               client_config["run_environment"] = parametros.banesco_url_test
            elif parametros.state=='enabled':
               client_config["run_environment"] = parametros.banesco_url_prod
            client_config['merchantid'] = parametros.banesco_merchant_id
            client_config['merchant_keyid'] = parametros.banesco_key
            client_config['merchant_secretkey'] = parametros.banesco_secret_key

            api_instance = PayerAuthenticationApi(client_config)
            return_data, status, body = api_instance.payer_auth_setup(requestObj)
            with open('/home/odoo/src/user/envio_setup.txt', 'w') as temp_file:
                temp_file.write("%s\n" % requestObj)
            
            with open('/home/odoo/src/user/setup_data.txt', 'w') as temp_file:
                temp_file.write("%s\n" % return_data)
            
            return return_data.consumer_authentication_information

        except Exception as e:
            #print("\nException when calling PayerAuthenticationApi->payer_auth_setup: %s\n" % e)
            with open('/home/odoo/src/user/error_setup.txt', 'w') as temp_file:
                temp_file.write("%s\n" % e)

            raise UserError(_(paymentInformationCardNumber + "\nException when calling PayerAuthenticationApi->payer_auth_setup: %s\n" % e))
        

        clientReferenceInformation = Riskv1decisionsClientReferenceInformation(
            code = clientReferenceInformationCode
        )

        orderInformationAmountDetailsCurrency = "USD"
        orderInformationAmountDetailsTotalAmount = data['amount']
        moneda= request.env['res.currency'].sudo().search([('id','=', data['currency_id'])])
        
        #convesrion a USD si la transaccion se hace en otra moneda
        if moneda.name !='USD':
            orderInformationAmountDetailsTotalAmount =  "{0:.2f}".format(moneda.inverse_rate * data['amount'])

        orderInformationAmountDetails = Riskv1authenticationsOrderInformationAmountDetails(
            currency = orderInformationAmountDetailsCurrency,
            total_amount = orderInformationAmountDetailsTotalAmount
        )

        
        #DATOS DEL CLIENTE        
        #usar dummy de acuerdo a las indicaciones
        if data['nombreCliente']=='' or data['apellidoCliente']=='':
           orderInformationBillToFirstName = 'NoReal' #dato dummy
           orderInformationBillToLastName =  'Name'   #dato dummy
        else:    
           orderInformationBillToFirstName = data['nombreCliente']#tx.partner_id.name ver si se puede usar el uitls de split 
           orderInformationBillToLastName =  data['apellidoCliente']
            
        pais_a_buscar = data['paisCliente'].capitalize()
        pais= request.env['res.country'].sudo().search([('name','=', pais_a_buscar)])
        email = False
        if '@' in data['emailCliente']:
          email= data['emailCliente']   
        
        orderInformationBillToAddress1 = data['calle'] or tx.partner_id.street
        orderInformationBillToLocality = data['ciudadCliente'] or tx.partner_id.city
        orderInformationBillToAdministrativeArea = data['estadoCliente'] or tx.partner_id.state_id.name #si da error pirmers dos letras en uppercase
        orderInformationBillToPostalCode = data['codPostalCliente'] or tx.partner_id.zip
        orderInformationBillToCountry = pais.code or tx.partner_id.country_id.code
        orderInformationBillToEmail = email or tx.partner_id.email or 'null@cybersource.com'
        orderInformationBillToPhoneNumber = data['telCliente'] or tx.partner_id.phone
        
        
        orderInformationBillTo = Riskv1authenticationsOrderInformationBillTo(
            address1 = orderInformationBillToAddress1,
            #address2 = orderInformationBillToAddress2,
            administrative_area = orderInformationBillToAdministrativeArea,
            country = orderInformationBillToCountry,
            locality = orderInformationBillToLocality,
            first_name = orderInformationBillToFirstName,
            last_name = orderInformationBillToLastName,
            phone_number = orderInformationBillToPhoneNumber,
            email = orderInformationBillToEmail,
            postal_code = orderInformationBillToPostalCode
        )

        orderInformation = Riskv1authenticationsOrderInformation(
            amount_details = orderInformationAmountDetails.__dict__,
            bill_to = orderInformationBillTo.__dict__
        )


        paymentInformationCard = Riskv1authenticationsPaymentInformationCard(
            type = paymentInformationCardType,
            expiration_month = paymentInformationCardExpirationMonth,
            expiration_year = paymentInformationCardExpirationYear,
            number = paymentInformationCardNumber
        )

        paymentInformation = Riskv1authenticationsPaymentInformation(
            card = paymentInformationCard.__dict__
        )

        buyerInformationMobilePhone = 1245789632
        buyerInformation = Riskv1authenticationsBuyerInformation(
            mobile_phone = buyerInformationMobilePhone
        )

        consumerAuthenticationInformationTransactionMode = "Retail"#"eCommerce"#"MOTO"
        consumerAuthenticationInformation = Riskv1decisionsConsumerAuthenticationInformation(
            transaction_mode = consumerAuthenticationInformationTransactionMode
        )

        requestObj = CheckPayerAuthEnrollmentRequest(
            client_reference_information = clientReferenceInformation.__dict__,
            order_information = orderInformation.__dict__,
            payment_information = paymentInformation.__dict__,
            buyer_information = buyerInformation.__dict__,
            consumer_authentication_information = consumerAuthenticationInformation.__dict__
        )


        requestObj = self.del_none(requestObj.__dict__)
        requestObj = json.dumps(requestObj)


        try:
            config_obj = configuration.Configuration()
            client_config = config_obj.get_configuration()
            if parametros.state=='test':
               client_config["run_environment"] = parametros.banesco_url_test
            elif parametros.state=='enabled':
               client_config["run_environment"] = parametros.banesco_url_prod
            client_config['merchantid'] = parametros.banesco_merchant_id
            client_config['merchant_keyid'] = parametros.banesco_key
            client_config['merchant_secretkey'] = parametros.banesco_secret_key

            api_instance = PayerAuthenticationApi(client_config)
            return_data, status, body = api_instance.check_payer_auth_enrollment(requestObj)
            with open('/home/odoo/src/user/envio_enroll.txt', 'w') as temp_file:
                temp_file.write("%s\n" % requestObj)

            with open('/home/odoo/src/user/enroll_data.txt', 'w') as temp_file:
                temp_file.write("%s\n" % return_data)


            #print('ENROLL')
            #return return_data
            #print (return_data.consumer_authentication_information)
            #print (return_data.status)
            auth_id= return_data.consumer_authentication_information.authentication_transaction_id
        except Exception as e:
            with open('/home/odoo/src/user/error_enroll.txt', 'w') as temp_file:
                temp_file.write("%s\n" % e)
 
            raise UserError(_('En estos momentos No se puede procesar su pago ENROLL'))


        clientReferenceInformationPartner = Riskv1decisionsClientReferenceInformationPartner(
            developer_id = clientReferenceInformationPartnerDeveloperId,
            solution_id = clientReferenceInformationPartnerSolutionId
        )

        clientReferenceInformation = Riskv1decisionsClientReferenceInformation(
            code = clientReferenceInformationCode,
            partner = clientReferenceInformationPartner.__dict__
        )

        #orderInformationAmountDetailsCurrency = "USD"
        #orderInformationAmountDetailsTotalAmount = "102.21"
        orderInformationAmountDetails = Riskv1authenticationsOrderInformationAmountDetails(
            currency = orderInformationAmountDetailsCurrency,
            total_amount = orderInformationAmountDetailsTotalAmount
        )


        orderInformationLineItems = []
        orderInformationLineItems1 = Riskv1authenticationresultsOrderInformationLineItems(
            unit_price = "10",
            quantity = 2,
            tax_amount = "32.40"
        )

        orderInformationLineItems.append(orderInformationLineItems1.__dict__)

        orderInformation = Riskv1authenticationresultsOrderInformation(
            amount_details = orderInformationAmountDetails.__dict__,
            line_items = orderInformationLineItems
        )

        paymentInformationCard = Riskv1authenticationresultsPaymentInformationCard(
            type = paymentInformationCardType,
            expiration_month = paymentInformationCardExpirationMonth,
            expiration_year = paymentInformationCardExpirationYear,
            number = paymentInformationCardNumber
        )

        paymentInformation = Riskv1authenticationresultsPaymentInformation(
            card = paymentInformationCard.__dict__
        )

        consumerAuthenticationInformationAuthenticationTransactionId = auth_id
        #consumerAuthenticationInformationSignedPares = "eNqdmFmT4jgSgN+J4D90zD4yMz45PEFVhHzgA2zwjXnzhQ984Nvw61dAV1"
        consumerAuthenticationInformation = Riskv1authenticationresultsConsumerAuthenticationInformation(
            authentication_transaction_id = consumerAuthenticationInformationAuthenticationTransactionId,
            #signed_pares = consumerAuthenticationInformationSignedPares
        )

        requestObj = ValidateRequest(
            client_reference_information = clientReferenceInformation.__dict__,
            order_information = orderInformation.__dict__,
            payment_information = paymentInformation.__dict__,
            consumer_authentication_information = consumerAuthenticationInformation.__dict__
        )


        requestObj = self.del_none(requestObj.__dict__)
        requestObj = json.dumps(requestObj)


        try:
            config_obj = configuration.Configuration()
            client_config = config_obj.get_configuration()
            if parametros.state=='test':
               client_config["run_environment"] = parametros.banesco_url_test
            elif parametros.state=='enabled':
               client_config["run_environment"] = parametros.banesco_url_prod
            client_config['merchantid'] = parametros.banesco_merchant_id
            client_config['merchant_keyid'] = parametros.banesco_key
            client_config['merchant_secretkey'] = parametros.banesco_secret_key

            api_instance = PayerAuthenticationApi(client_config)
            return_data, status, body = api_instance.validate_authentication_results(requestObj)

            #print('VALIDATION')
            #print (return_data.consumer_authentication_information)
            #print (return_data.status)
            #'AUTHENTICATION_FAILED' falla
            #'AUTHENTICATION_SUCCESSFUL' exito se puede realizar la autorizacion
            with open('/home/odoo/src/user/envio_validacion.txt', 'w') as temp_file:
                temp_file.write("%s\n" % requestObj)

            with open('/home/odoo/src/user/validation_data.txt', 'w') as temp_file:
                temp_file.write("%s\n" % return_data)
    
            return return_data
        except Exception as e:
            with open('/home/odoo/src/user/error_validate.txt', 'w') as temp_file:
                temp_file.write("%s\n" % e)

            raise UserError(_('En estos momentos No se puede procesar su pago VAlidate'))

