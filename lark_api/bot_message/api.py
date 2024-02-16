#! /usr/bin/env python3.8
import os
import logging
import requests

from commons.lark_api_urls import MESSAGE_URI
from lark_api.auth.api import authorize_tenant_access_token

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


class MessageApiClient(object):
    def __init__(self, app_id, app_secret, lark_host):
        self._app_id = app_id
        self._app_secret = app_secret
        self._lark_host = lark_host
        self._tenant_access_token = ""
        self._latest_message_id = ""

    @property
    def tenant_access_token(self):
        return self._tenant_access_token

    def send_message_with_open_id(self, open_id, msg_type, content):
        self.send("open_id", open_id, msg_type, content)

    def send(self, receive_id_type, receive_id, msg_type, content):
        # send message to user, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        self._authorize_tenant_access_token()
        url = "{}{}?receive_id_type={}".format(
            self._lark_host, MESSAGE_URI, receive_id_type
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.tenant_access_token,
        }

        req_body = {
            "receive_id": receive_id,
            "content": content,
            "msg_type": msg_type,
        }
        resp = requests.post(url=url, headers=headers, json=req_body)
        self._latest_message_id = resp.json()["data"]["message_id"]
        MessageApiClient._check_error_response(resp)

    def update_message(self, updated_message):
        self._authorize_tenant_access_token()
        url = f'{self._lark_host}{MESSAGE_URI}/{self._latest_message_id}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.tenant_access_token,
        }
        req_body = {
            "content": updated_message
        }
        resp = requests.patch(url=url, headers=headers, json=req_body)
        MessageApiClient._check_error_response(resp)

    def _authorize_tenant_access_token(self):
        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        response = authorize_tenant_access_token()
        MessageApiClient._check_error_response(response)
        self._tenant_access_token = response.json().get("tenant_access_token")

    @staticmethod
    def _check_error_response(resp):
        # check if the response contains error information
        if resp.status_code != 200:
            resp.raise_for_status()
        response_dict = resp.json()
        code = response_dict.get("code", -1)
        if code != 0:
            logging.error(response_dict)
            raise LarkException(code=code, msg=response_dict.get("msg"))


class LarkException(Exception):
    def __init__(self, code=0, msg=None):
        self.code = code
        self.msg = msg

    def __str__(self) -> str:
        return "{}:{}".format(self.code, self.msg)


    __repr__ = __str__


