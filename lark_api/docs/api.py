import os
from commons.lark_api_urls import LARK_HOST, DOCS_CREATE_URI
from lark_api.auth.api import authorize_tenant_access_token, authorize_user_access_token
from constants import startup_new_docs_template
import requests
import json

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

def create_startup_pitching_document(receive_id_type, receive_id):
    tenant_access_token_request = authorize_tenant_access_token(APP_ID, APP_SECRET)
    print(authorize_user_access_token(receive_id).json())
    tenant_access_token = tenant_access_token_request.json().get("tenant_access_token")
    url = "{}{}".format(
        LARK_HOST, DOCS_CREATE_URI
    )
    print(url)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tenant_access_token,
    }
    req_body = {
        "FolderToken": None,
        "Content": json.dumps(startup_new_docs_template)
    }

    return requests.post(url=url, headers=headers, json=req_body)