import json
import os
import requests
import sseclient
from dotenv import load_dotenv
from constants import *

load_dotenv()

from constants import *


class BotpressClient:
    def __init__(self, api_id=None, user_key=None):
        self.api_id = api_id or os.getenv("CHAT_API_ID")
        self.user_key = user_key or os.getenv("USER_KEY")
        self.base_url = f"{BASE_URI}/{self.api_id}"
        self.headers = {
            **HEADERS,
            "x-user-key": self.user_key,
        }

    def _request(self, method, path, json=None):
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, headers=self.headers, json=json)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return response.status_code, response.text

    # --- Core API Methods ---

    def get_user(self):
        return self._request("GET", "/users/me")
    
    def create_user(self, user_data):
        return self._request("POST", "/users", json=user_data)

    def create_conversation(self):
        return self._request("POST", "/conversations", json={"body": {}})

    def list_conversations(self):
        return self._request("GET", "/conversations")

    def create_message(self, message, conversation_id):
        payload = {
            "payload": {"type": "text", "text": message},
            "conversationId": conversation_id,
        }
        return self._request("POST", "/messages", json=payload)

    def list_messages(self, conversation_id):
        return self._request("GET", f"/conversations/{conversation_id}/messages")

    def listen_conversation(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/listen"
        # response = requests.get(, stream=True, )
        for event in sseclient.SSEClient(url, headers=self.headers):
            print(event.data)
            if event.data == "ping":
                continue
            data = json.loads(event.data)["data"]
            is_bot = data["isBot"]
            yield data["payload"]["text"]
