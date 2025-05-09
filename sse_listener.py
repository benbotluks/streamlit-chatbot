import json
from client import listen_conversation
from constants import CONVERSATION_ID

client = listen_conversation(conversation_id=CONVERSATION_ID)

print("Listening for SSE events...\n")

for event in client:
    data = json.loads(event.data)["data"]
    is_bot = data["isBot"]
    print(f"{'Winona' if is_bot else 'Ben'}: {data['payload']['text']}\n")
