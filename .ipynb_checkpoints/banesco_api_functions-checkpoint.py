from CyberSource import *
import os
import json
from importlib.machinery import SourceFileLoader

config_file =  "src/user/payment_banesco/controllers/Configuration.py"
configuration = SourceFileLoader("module.name", config_file).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d


#capturar una transaccion para confirmarla
def capture_payment(transaction_id):
    #api_payment_response = process_payment.simple_authorizationinternet(False)
    id = transaction_id

    clientReferenceInformationCode = "TC50171_3"
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    orderInformationAmountDetailsTotalAmount = "98.25"
    orderInformationAmountDetailsCurrency = "USD"
    orderInformationAmountDetails = Ptsv2paymentsidcapturesOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformation = Ptsv2paymentsidcapturesOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__
    )

    requestObj = CapturePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        order_information = orderInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)


    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = CaptureApi(client_config)
        return_data, status, body = api_instance.capture_payment(requestObj, id)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        return return_data
    except Exception as e:
        print("\nException when calling CaptureApi->capture_payment: %s\n" % e)

#anular transaccion
def void_payment(payment_id):
    #api_payment_response = process_payment.simple_authorizationinternet(False)
    id = payment_id

    clientReferenceInformationCode = "Anulación"
    clientReferenceInformation = Ptsv2paymentsidreversalsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    requestObj = VoidPaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)


    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = VoidApi(client_config)
        return_data, status, body = api_instance.void_payment(requestObj, id)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        return return_data
    except Exception as e:
        print("\nException when calling VoidApi->void_payment: %s\n" % e)
        

def refund_payment(payment_id):
    #api_payment_response = process_payment.simple_authorizationinternet(True)
    id = payment_id

    clientReferenceInformationCode = "TC50171_3"
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    orderInformationAmountDetailsTotalAmount = "10"
    orderInformationAmountDetailsCurrency = "USD"
    orderInformationAmountDetails = Ptsv2paymentsidcapturesOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformation = Ptsv2paymentsidrefundsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__
    )

    requestObj = RefundPaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        order_information = orderInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)


    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = RefundApi(client_config)
        return_data, status, body = api_instance.refund_payment(requestObj, id)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        return return_data
    except Exception as e:
        print("\nException when calling RefundApi->refund_payment: %s\n" % e)        
        
        #if __name__ == "__main__":
#    capture_payment('6574616796136914604953')


