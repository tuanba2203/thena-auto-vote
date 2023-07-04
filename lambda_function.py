import os
import json
import boto3
import base64
import requests
from web3.auto import w3
from eth_account.messages import encode_defunct
from botocore.exceptions import ClientError

wallet_address = os.environ['wallet_address']
thena_api_url = os.eviron['thena_api_url']
bsc_dataseed_url = os.eviron['bsc_dataseed_url']

def get_wallet_secret(secret_name, secret_key):
    encrypted_wallet_secret_str = os.environ['wallet_secret_strings']
    wallet_secret_str = base64.b64decode(encrypted_wallet_secret_str).decode('utf-8')
    return wallet_secret_str


def sign_message(private_, raw_message):
    message = encode_defunct(text=raw_message)
    signed_message = w3.eth.account.sign_message(message, private_key=private_)
    return signed_message
    
    
def get_thena_asset_data():
    response = requests.get(thena_api_url+"/api/v1/assets")
    print("Fusion Data: ", json.loads(response.text))
    if(json.loads(response.text)['success'] is True):
        return json.loads(response.text)['data']
    else:
        return None
    
def get_thena_fusion_data():
    response = requests.get(thena_api_url+"/api/v1/fusions")
    print("Fusion Data: ", json.loads(response.text))
    if(json.loads(response.text)['success'] is True):
        return json.loads(response.text)['data']
    else:
        return None
        

def lambda_handler(event, context):
    print(get_thena_asset_data())
    
    signed_message = sign_message(private_, raw_message)
    print("Signed mess: ", signed_message.signature.hex())
    
    
    
    return {
        'statusCode': 200,
        'body': signed_message.signature.hex()
    }
