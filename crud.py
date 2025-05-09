import os
import requests
import sseclient
from dotenv import load_dotenv
from constants import *

load_dotenv()

chat_id = os.getenv("CHAT_API_ID")
chat_endpoint = f"{BASE_URI}/{chat_id}"


def get_auth_headers():
    """Builds headers with auth key"""
    return {
        **HEADERS,
        "x-user-key": os.getenv("USER_KEY"),
    }

auth_headers = get_auth_headers()

def safe_request(method, path, json=None):
    """Wrapper for GET/POST requests with error handling"""
    url = f"{chat_endpoint}{path}"
    headers = auth_headers
    resp = requests.request(method, url, headers=headers, json=json)

    try:
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError:
        return resp.status_code, resp.text


# ----- API Functions -----

def create_user(user_data):
    return safe_request("POST", "/users", json=user_data)


def create_conversation():
    return safe_request("POST", "/conversations", json={"body": {}})


def list_conversations():
    return safe_request("GET", "/conversations")


def create_message(message):
    payload = {
        "payload": {"type": "text", "text": message},
        "conversationId": CONVERSATION_ID,
    }
    return safe_request("POST", "/messages", json=payload)


def list_messages(conversation_id):
    return safe_request("GET", f"/conversations/{conversation_id}/messages")


def listen_conversation(conversation_id):
    url = f"{chat_endpoint}/conversations/{conversation_id}/listen"
    headers = auth_headers
    return sseclient.SSEClient(requests.get(url, stream=True, headers=headers))
