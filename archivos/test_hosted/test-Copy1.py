from uuid import uuid4
from datetime import datetime, timezone
import requests


transaction_uuid = uuid4().hex




url = "https://testsecureacceptance.cybersource.com/pay"

payload={'access_key': '62faa2c32b7039bab7f658c14339bdfb',
'profile_id': '74EDC3E4-2B1F-4EAA-BE80-6A8AA95FA648',
'transaction_uuid': transaction_uuid,
'signed_field_names': ' access_key,profile_id,transaction_uuid,signed_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,merchant_defined_data5,merchant_defined_data6,customer_ip_address,bill_to_address_city,bill_to_address_country,bill_to_address_line1,bill_to_address_state,bill_to_email,bill_to_forename,bill_to_phone,bill_to_surname',
'merchant_defined_data5': ' WEB',
'merchant_defined_data6': ' LOVABLE',
'customer_ip_address': ' 190.5.88.139',
'bill_to_address_city': ' Galván',
'bill_to_address_country': ' DO',
'bill_to_address_line1': ' Calle falsa',
'bill_to_address_state': ' Baoruco ',
'bill_to_email': ' asd@gmail.com',
'bill_to_forename': ' tester',
'bill_to_surname': ' test',
'bill_to_phone': ' 13123',
'signed_date_time': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
'locale': ' es-es',
'transaction_type': ' sale',
'reference_number': ' 500000101',
'amount': ' 2715.50',
'currency': ' DOP',
'signature': ' Gee9b05LsHvLYokYd8eof5bZffgMtQew0lgj5HushQc='}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)



def generate_cybersource_sa_signature(payload):
    """
    Generate an HMAC SHA256 signature for the CyberSource Secure Acceptance payload

    Args:
        payload (dict): The payload to be sent to CyberSource
    Returns:
        str: The signature
    """
    # This is documented in certain CyberSource sample applications:
    # http://apps.cybersource.com/library/documentation/dev_guides/Secure_Acceptance_SOP/html/wwhelp/wwhimpl/js/html/wwhelp.htm#href=creating_profile.05.6.html
    keys = payload['signed_field_names'].split(',')
    message = ','.join('{}={}'.format(key, payload[key]) for key in keys)

    digest = hmac.new(
        settings.CYBERSOURCE_SECURITY_KEY.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256,
    ).digest()

    return b64encode(digest).decode('utf-8') 