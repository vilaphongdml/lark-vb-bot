import os
from commons.lark_api_urls import LARK_HOST, DOCS_CREATE_URI, UPDATE_DOCUMENT_PERMISSION 
from lark_api.auth.api import authorize_tenant_access_token
from lark_api.base.api import get_startup_record_by_user
from constants import get_startup_new_docs_template
import requests
import json

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

def create_startup_pitching_document(open_id):
    tenant_access_token_request = authorize_tenant_access_token()
    tenant_access_token = tenant_access_token_request.json().get("tenant_access_token")
    url = "{}{}".format(
        LARK_HOST, DOCS_CREATE_URI
    )

    # get startup name
    startup_name = get_startup_record_by_user(open_id)['fields']['Startup Name']

    # get_startup_new_docs_template
    startup_new_docs_template = get_startup_new_docs_template(startup_name)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tenant_access_token,
    }
    req_body = {
        "FolderToken": "B2l4fItPdlZ9d2dMKv2lr5csgqb",
        "Content": json.dumps(startup_new_docs_template)
    }

    return requests.post(url=url, headers=headers, json=req_body)

def create_docs(content):
    tenant_access_token_request = authorize_tenant_access_token()
    tenant_access_token = tenant_access_token_request.json().get("tenant_access_token")
    url = "{}{}".format(
        LARK_HOST, DOCS_CREATE_URI
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tenant_access_token,
    }
    req_body = {
        "FolderToken": "Sgyif24oHlP8qwd8MgolcjdTg9f",
        "Content": content
    }

    return requests.post(url=url, headers=headers, json=req_body)

def add_document_user_permission(docs_token, open_id, permission):
    tenant_access_token_request = authorize_tenant_access_token()
    tenant_access_token = tenant_access_token_request.json().get("tenant_access_token")
    url = f'{LARK_HOST}{UPDATE_DOCUMENT_PERMISSION}{docs_token}/members/?type=doc'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tenant_access_token,
    }
    req_body = {
        "member_type": "openid",
        "member_id": open_id,
        "perm": permission
    }

    return requests.post(url=url, headers=headers, json=req_body)
