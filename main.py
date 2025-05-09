from client import *
from constants import *

client = BotpressClient()
conversations = client.list_messages(CONVERSATION_ID)
print(conversations)