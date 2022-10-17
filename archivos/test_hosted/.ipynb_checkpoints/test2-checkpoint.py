import http.client
import mimetypes
from codecs import encode
from uuid import uuid4
from datetime import datetime, timezone

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

payload={'access_key': ' 8a26523e83db326b88fb0f39502ff0b7',
'profile_id': ' 6CF18110-BA37-4430-831B-EBD3B820ACE8',
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
    'Host' : "https://testsecureacceptance.cybersource.com/pay"
}
payload['signature'] = to_send['signature']
         
#response = requests.request("POST", url, headers=headers, data=payload, files=files)

#print(response.text)




conn = http.client.HTTPSConnection("testsecureacceptance.cybersource.com")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T' #????
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=access_key;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode('62faa2c32b7039bab7f658c14339bdfb'))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=profile_id;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("74EDC3E4-2B1F-4EAA-BE80-6A8AA95FA648"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=transaction_uuid;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(uuid4().hex))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=signed_field_names;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("access_key,profile_id,transaction_uuid,signed_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,merchant_defined_data5,merchant_defined_data6,customer_ip_address,bill_to_address_city,bill_to_address_country,bill_to_address_line1,bill_to_address_state,bill_to_email,bill_to_forename,bill_to_phone,bill_to_surname"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=merchant_defined_data5;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("WEB"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=merchant_defined_data6;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("LOVABLE"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=customer_ip_address;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("190.5.88.139"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_address_city;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("Galván"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_address_country;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("DO"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_address_line1;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("Calle falsa"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_address_state;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("Baoruco"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_email;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("asd@gmail.com"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_forename;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("tester"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_surname;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("test"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=bill_to_phone;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("13123"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=signed_date_time;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=locale;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("es-es"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=transaction_type;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("sale"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=reference_number;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("500000101"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=amount;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("2715.50"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=currency;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("DOP"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=signature;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(to_send['signature']))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
   'Content-type': 'multipart/form-data; boundary={}'.format(boundary), 
   'Host' : "https://testsecureacceptance.cybersource.com",
}

conn.request("POST", "/pay", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))