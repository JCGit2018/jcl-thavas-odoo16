from uuid import uuid4
from datetime import datetime, timezone
import requests

#import datetime
from base64 import b64encode
from hashlib import sha256
import hmac


transaction_uuid = uuid4().hex



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


def sign_fields_to_context(fields, context):
    """
    Builds the list of file names and data to sign, and created the
    signature required by CyberSource.
    """
    
    CYBERSOURCE_SECRET_KEY = '7da6b7dc11374e72b6fefa30c66f0766738aab3d2d8d4897b5eae4597a5153b74594a9789a31442ca26b73151da9cc9714a87a0b13bf4bd39a7cdf794ea3a76b17724df25e0a4974bd8b34db570e37a2db15f8f50f6849878c85fca6d10c7da7f7978d4acb6345a5a7d5eac78536df6afe219a7d0bd644b1aa2ee73032fed471'
    
    #fields['signed_date_time'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signed_field_names = []
    data_to_sign = []
    for key, value in fields.items():
        signed_field_names.append(key)
    #print(fields)
    #print()
    # After adding all the included fields, we need to also add
    # `unsigned_field_names` and `signed_field_names` to the data
    # to be signed.
    #signed_field_names.append('unsigned_field_names')
    #fields['unsigned_field_names'] = ''
    #signed_field_names.append('signed_field_names')
    #fields['signed_field_names'] = ','.join(signed_field_names)

    # Build the fields into a list to sign, which will become
    # a string when joined by a comma
    for key, value in fields.items():
        data_to_sign.append(f'{key}={value}')
    
    #print(data_to_sign)
    
    context['fields'] = fields
    context['signature'] = create_sha256_signature(
        CYBERSOURCE_SECRET_KEY,
        ','.join(data_to_sign),
    )
    #context['url'] = settings.CYBERSOURCE_URL

    return context








url = "https://testsecureacceptance.cybersource.com/pay"

payload={'access_key': '8a26523e83db326b88fb0f39502ff0b7',
'profile_id': '6CF18110-BA37-4430-831B-EBD3B820ACE8',
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
'currency': ' DOP'}
#'signature': ' Gee9b05LsHvLYokYd8eof5bZffgMtQew0lgj5HushQc='}
         
context = dict()
#print(response.text)
to_send= sign_fields_to_context(payload,context)         
files=[

]
headers = {
 #   'Host' : "https://testsecureacceptance.cybersource.com",
 #   'Content-Type': 'application/x-www-form-urlencoded'
}
payload['signature'] = to_send['signature']
         
response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
