from commons.lark_api_urls import TENANT_ACCESS_TOKEN_URI, LARK_HOST, USER_ACCESS_TOKEN_URI
import requests

def authorize_tenant_access_token(app_id, app_secret):
    '''
    This function is for getting token for bot app
    '''
    # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
    url = "{}{}".format(LARK_HOST, TENANT_ACCESS_TOKEN_URI)
    req_body = {"app_id": app_id, "app_secret": app_secret}
    return requests.post(url, req_body)

def authorize_user_access_token(receive_id):
    url = "{}{}".format(LARK_HOST, USER_ACCESS_TOKEN_URI)
    req_body = {"grant_type": "open_id", "code": receive_id}
    return requests.post(url, req_body)