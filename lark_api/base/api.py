from lark_api.auth.api import authorize_tenant_access_token
import requests
import json
import os
from commons.lark_api_urls import LARK_HOST, BASE_URI

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
STARTUP_TABLE_ID = os.getenv("STARTUP_TABLE_ID")
APP_TOKEN = os.getenv("APP_TOKEN")

def get_startup_record_by_user(open_id):
    tenant_access_token_request = authorize_tenant_access_token()
    tenant_access_token = tenant_access_token_request.json().get("tenant_access_token")
    url = f'{LARK_HOST}{BASE_URI}{APP_TOKEN}/tables/{STARTUP_TABLE_ID}/records'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tenant_access_token,
    }
    response = requests.get(url=url, headers=headers)
    response_data = response.json()['data']['items']
    filtered_records = filter(lambda record: record['fields']['Created By']['id'] == open_id, response_data)
    found_record = next(filtered_records, None)  # Get the first matching record only
    return found_record


def update_record(record_id, record_data):
    tenant_access_token_request = authorize_tenant_access_token()
    tenant_access_token = tenant_access_token_request.json().get("tenant_access_token")
    url = f'{LARK_HOST}{BASE_URI}{APP_TOKEN}/tables/{STARTUP_TABLE_ID}/records/{record_id}/?user_id_type=open_id'
    print(tenant_access_token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tenant_access_token,
    }
    print("update record_data")
    print(record_data)
    response = requests.put(url=url, headers=headers, json=record_data)
    print("update response")
    print(response.json())
    return response