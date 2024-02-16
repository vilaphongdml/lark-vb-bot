#!/usr/bin/env python3.8

import os
import logging
import requests
from lark_api.bot_message.api import MessageApiClient
from lark_api.docs.api import create_startup_pitching_document, add_document_user_permission, create_docs
from lark_api.base.utils import update_pitching_document
from event import MessageReceiveEvent, UrlVerificationEvent, EventManager, UserAndBotChatCreateEvent
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
from constants import startup_registration_form, investor_registration_form, get_docs_redirection_form,\
    successful_registration_form, get_recent_news, news_template, get_create_news_card
import json

# load env parameters form file named .env
load_dotenv(find_dotenv())

app = Flask(__name__)

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
LARK_HOST = os.getenv("LARK_HOST")

# init service
message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)
event_manager = EventManager()


@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    if message.message_type != "text":
        logging.warn("Other types of messages have not been processed yet")
        return jsonify()
        # get open_id and text_content
    open_id = sender_id.open_id
    print("open_id")
    print(open_id)
    message = message.content
    # echo text message
    if 'startup registration form' in message.lower():
        message = startup_registration_form
        response = message_api_client.send_message_with_open_id(open_id, 'interactive', json.dumps(message))
        
        ## FOR RECORDING ONLY
        import time
        time.sleep(5)
        # update startup registration form
        updated_registration_card = json.dumps(successful_registration_form)
        message_api_client.update_message(updated_registration_card)
        # create documents
        create_docs_response = create_startup_pitching_document(open_id)
        create_docs_response_json = json.loads(create_docs_response.content.decode('utf-8'))
        docs_url = create_docs_response_json['data']['url']
        docs_token = create_docs_response_json['data']['objToken']
        # update document permission
        add_document_user_permission(docs_token, open_id, 'full_access')
        # update pitching document url in base
        message_api_client.send_message_with_open_id(open_id, 'interactive', json.dumps(get_docs_redirection_form(docs_url)))

    elif 'investor registration form' in message.lower():
        message = investor_registration_form
        message_api_client.send_message_with_open_id(open_id, 'interactive', json.dumps(message))
        
        ## FOR RECORDING ONLY
        import time
        time.sleep(6)
        # update startup registration form
        updated_registration_card = json.dumps(successful_registration_form)
        message_api_client.update_message(updated_registration_card)

        message = "{\"text\":\"Thank you for your joining us! Here are recent news of the industries you subscribed that you might be interested in.\"}"
        message_api_client.send_message_with_open_id(open_id, 'text', message)

        # send recent news
        recent_news = get_recent_news()
        for news in recent_news:
            message_api_client.send_message_with_open_id(open_id, 'interactive', json.dumps(news))
    
    elif 'create a news' in message.lower():
        create_docs_response = create_docs(json.dumps(news_template))
        create_docs_response_json = json.loads(create_docs_response.content.decode('utf-8'))
        print(create_docs_response_json)
        docs_url = create_docs_response_json['data']['url']
        message = get_create_news_card(docs_url)
        message_api_client.send_message_with_open_id(open_id, 'interactive', json.dumps(message))

    elif 'registered' in message.lower():
        # update startup registration form
        updated_registration_card = json.dumps(successful_registration_form)
        message_api_client.update_message(updated_registration_card)
        # create documents
        create_docs_response = create_startup_pitching_document(open_id)
        create_docs_response_json = json.loads(create_docs_response.content.decode('utf-8'))
        docs_url = create_docs_response_json['data']['url']
        docs_token = create_docs_response_json['data']['objToken']
        # update document permission
        add_document_user_permission(docs_token, open_id, 'full_access')
        # update pitching document url in base
        message_api_client.send_message_with_open_id(open_id, 'interactive', json.dumps(get_docs_redirection_form(docs_url)))
    else:
        message_api_client.send_message_with_open_id(open_id, 'text', "Sorry, I can't comphrend your message. :<")
    return jsonify()

@event_manager.register("p2p_chat_create")
def p2p_chat_create_event_handler(req_data: UserAndBotChatCreateEvent):
    open_id = req_data.event.open_chat_id
    message = startup_registration_form
    message_api_client.send_message_with_open_id(open_id, 'interactive', json.dumps(message))
    return jsonify()


@app.errorhandler
def msg_error_handler(ex):
    logging.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


@app.route("/", methods=["POST"])
def callback_event_handler():
    # init callback instance and handle
    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)

    return event_handler(event)


if __name__ == "__main__":
    # init()
    app.run(host="0.0.0.0", port=3000, debug=True)


