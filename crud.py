import requests
from constants import *
import sseclient

import os
from dotenv import load_dotenv

load_dotenv()

chat_id = os.getenv("CHAT_API_ID")
chat_endpoint = f"{BASE_URI}/{chat_id}"


def create_user(user_data):
    response = requests.post(f"{chat_endpoint}/users", json=user_data, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text


def create_conversation():
    headers = {**HEADERS, "x-user-key": os.getenv("USER_KEY")}

    response = requests.post(
        f"{chat_endpoint}/conversations", headers=headers, json={"body": {}}
    )
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text


def list_conversations():
    headers = {**HEADERS, "x-user-key": os.getenv("USER_KEY")}

    response = requests.get(
        f"{chat_endpoint}/conversations", headers=headers, json={"body": {}}
    )

    return response.json()


def create_message(message):
    headers = {
        **HEADERS,
        "x-user-key": os.getenv("USER_KEY"),
    }

    payload = {
        "payload": {"type": "text", "text": message},
        "conversationId": CONVERSATION_ID,
    }
    response = requests.post(f"{chat_endpoint}/messages", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text


def list_messages(conversation_id):
    headers = {
        **HEADERS,
        "x-user-key": os.getenv("USER_KEY"),
    }

    response = requests.get(
        f"{chat_endpoint}/conversations/{conversation_id}/messages",
        headers=headers,
    )

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text


def listen_conversation(conversation_id):
    headers = {
        **HEADERS,
        "x-user-key": os.getenv("USER_KEY"),
    }
    client = sseclient.SSEClient(
        f"{chat_endpoint}/conversations/{conversation_id}/listen",
        headers=headers,
        # stream=True
    )
    return client
