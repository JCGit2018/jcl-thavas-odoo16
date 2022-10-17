from uuid import uuid4
from datetime import datetime, timezone


#import datetime
from base64 import b64encode, b64decode
from hashlib import sha256
import hashlib
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
    #context['signature'] = create_sha256_signature(
    #    CYBERSOURCE_SECRET_KEY,
    #    ','.join(data_to_sign),
    #)
    #print(','.join(data_to_sign))
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



payload1={'access_key': '62faa2c32b7039bab7f658c14339bdfb',
'profile_id': '74EDC3E4-2B1F-4EAA-BE80-6A8AA95FA648',
'transaction_uuid': '633343a2bc6c4',
'signed_field_names': 'access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,merchant_defined_data1,merchant_defined_data2,merchant_defined_data3,merchant_defined_data4,merchant_defined_data5,merchant_defined_data6,merchant_defined_data7,merchant_defined_data8,merchant_defined_data10,merchant_defined_data15,merchant_defined_data19,merchant_defined_data17,merchant_defined_data21,merchant_defined_data24,merchant_defined_data28',
'unsigned_field_names':'',
#'signed_date_time': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),         
'signed_date_time': '2022-09-27T18:40:34Z',         
'locale': 'en',
'transaction_type': 'authorization',
'reference_number': '1664304037055',
'amount': '100.00',
'currency': 'USD',
"merchant_defined_data1": 'bc_5808831146',
"merchant_defined_data2": 'WEB',
"merchant_defined_data3": '1664213208603', #referencia de venta
"merchant_defined_data4": 'RETAIL',
"merchant_defined_data5": 'PADEL',#nombre del comercio
"merchant_defined_data6": "CATEGORY1", #categoria de productos
"merchant_defined_data7": "JOE", #datos del cliente 
"merchant_defined_data8": "NO", #Compra a tercero
"merchant_defined_data10": "YES", #Email was confirmed
"merchant_defined_data15": "Windows 10 64-bit",#Sistema Operativo utilizado en la orden
"merchant_defined_data19": "1600811150",#fecha de la transac (timestamp)???
"merchant_defined_data17": "9NKKSEV7",#Codigo de Autorizacion
"merchant_defined_data21": "148",#numero factura
"merchant_defined_data24": "NO",#TOKENIZATION
"merchant_defined_data28": "001" #sucursal 
         }

CYBERSOURCE_SECRET_KEY = '7da6b7dc11374e72b6fefa30c66f0766738aab3d2d8d4897b5eae4597a5153b74594a9789a31442ca26b73151da9cc9714a87a0b13bf4bd39a7cdf794ea3a76b17724df25e0a4974bd8b34db570e37a2db15f8f50f6849878c85fca6d10c7da7f7978d4acb6345a5a7d5eac78536df6afe219a7d0bd644b1aa2ee73032fed471'

print(generate_signature(CYBERSOURCE_SECRET_KEY,**payload1))

'62faa2c32b7039bab7f658c14339bdfb,74EDC3E4-2B1F-4EAA-BE80-6A8AA95FA648,53612,access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,,2022-09-21T18:28:49Z,en,authorization,1663784934035,'
'100.00,USD,Submit'

    

    
'access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,bill_to_address_city,bill_to_address_country,bill_to_address_line1,bill_to_address_state,bill_to_email,bill_to_forename,bill_to_phone,bill_to_surname,bill_to_address_postal_code,ship_to_address_city,ship_to_address_country,ship_to_address_line1,ship_to_address_state,ship_to_email,ship_to_forename,ship_to_phone,ship_to_surname,ship_to_address_postal_code,merchant_defined_data1,merchant_defined_data2,merchant_defined_data3,merchant_defined_data4,merchant_defined_data5,merchant_defined_data6,merchant_defined_data7,merchant_defined_data8,merchant_defined_data10,merchant_defined_data15,merchant_defined_data19,merchant_defined_data17,merchant_defined_data21,merchant_defined_data24,merchant_defined_data28'    

'''
    <input type="text" id="access_key" name="access_key" value="62faa2c32b7039bab7f658c14339bdfb"/>
<input type="text" id="profile_id" name="profile_id" value="74EDC3E4-2B1F-4EAA-BE80-6A8AA95FA648"/>
<input type="text" id="transaction_uuid" name="transaction_uuid" value="632ded3867f8b"/>
<input type="text" id="signed_field_names" name="signed_field_names" value="access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency"/>
<input type="text" id="unsigned_field_names" name="unsigned_field_names" value=""/>
<input type="text" id="signed_date_time" name="signed_date_time" value="2022-09-23T17:30:32Z"/>
<input type="text" id="locale" name="locale" value="en"/>
<input type="text" id="transaction_type" name="transaction_type" value="authorization"/>
<input type="text" id="reference_number" name="reference_number" value="1663954758872"/>
<input type="text" id="amount" name="amount" value="100.00"/>
<input type="text" id="currency" name="currency" value="USD"/>
<input type="text" id="submit" name="submit" value="Submit"/>
<input type="text" id="signature" name="signature" value="6t4LyZR5zlCjXiK7AzmL/myxWiJ1pXU9bUYyJSCXkuk="/>
6t4LyZR5zlCjXiK7AzmL/myxWiJ1pXU9bUYyJSCXkuk=
<input type="submit" id="submit" value="Confirm"/>
0kLRbBJyz259jIBaF2TbOrGNwFXDm4v+DIJokxnPHm8=
0kLRbBJyz259jIBaF2TbOrGNwFXDm4v+DIJokxnPHm8=
'''


