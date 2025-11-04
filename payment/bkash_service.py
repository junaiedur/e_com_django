import requests
from django.conf import settings
import json

# bKash API এন্ডপয়েন্ট
TOKEN_URL = f"{settings.BKASH_BASE_URL}/token/grant"
CREATE_PAYMENT_URL = f"{settings.BKASH_BASE_URL}/payment/create"
EXECUTE_PAYMENT_URL = f"{settings.BKASH_BASE_URL}/payment/execute"

# bKash হেডার
def get_bkash_headers(id_token=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-app-key": settings.BKASH_APP_KEY,
    }
    if id_token:
        headers["Authorization"] = id_token
    return headers

# ১. টোকেন জেনারেট করা
def get_bkash_token():
    payload = {
        "app_key": settings.BKASH_APP_KEY,
        "app_secret": settings.BKASH_APP_SECRET
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "username": settings.BKASH_USERNAME,
        "password": settings.BKASH_PASSWORD
    }
    try:
        response = requests.post(TOKEN_URL, json=payload, headers=headers, timeout=10)
        response_data = response.json()
        if response.status_code == 200 and 'id_token' in response_data:
            return response_data['id_token']
        else:
            print(f"bKash Token Error: {response_data.get('errorMessage', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"bKash Token Exception: {str(e)}")
        return None

# ২. পেমেন্ট তৈরি করা
def create_payment(amount, order_id, callback_url):
    id_token = get_bkash_token()
    if not id_token:
        return {"status": "error", "message": "Could not get bKash token"}

    payload = {
        "mode": "0011",
        "payerReference": str(order_id), # আপনার অর্ডার আইডি
        "callbackURL": callback_url,
        "amount": str(amount),
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": str(order_id) # আপনার ইনভয়েস/অর্ডার আইডি
    }
    
    try:
        response = requests.post(CREATE_PAYMENT_URL, json=payload, headers=get_bkash_headers(id_token), timeout=10)
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get('paymentID'):
            return {"status": "success", "paymentID": response_data['paymentID'], "bkashURL": response_data['bkashURL']}
        else:
            return {"status": "error", "message": response_data.get('errorMessage', 'Create payment failed')}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ৩. পেমেন্ট এক্সিকিউট করা
def execute_payment(payment_id):
    id_token = get_bkash_token()
    if not id_token:
        return {"status": "error", "message": "Could not get bKash token"}

    payload = { "paymentID": payment_id }
    
    try:
        response = requests.post(EXECUTE_PAYMENT_URL, json=payload, headers=get_bkash_headers(id_token), timeout=10)
        response_data = response.json()

        if response.status_code == 200 and response_data.get('trxID'):
            return {"status": "success", "data": response_data}
        else:
            return {"status": "error", "message": response_data.get('errorMessage', 'Execute payment failed')}
    except Exception as e:
        return {"status": "error", "message": str(e)}