from client import BotpressClient
import streamlit as st
from constants import CONVERSATION_ID

st.title("Botpress Front-end for Streamlit")

client = BotpressClient(
    api_id=st.secrets["CHAT_API_ID"], user_key=st.secrets["USER_KEY"]
)

user = client.get_user()
user_id = user["user"]["id"]

print("user id: ", user_id)

if "messages" not in st.session_state:
    st.session_state.messages = []
    messages = client.list_messages(CONVERSATION_ID)
    next_token = messages["meta"]["nextToken"]

    for message in messages["messages"][::-1]:
        role = "user" if message["userId"] == user_id else "assistant"
        text = message["payload"]["text"]

        st.session_state.messages.append({"role": role, "content": text})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("*wine*-d it up"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    client.create_message(prompt, conversation_id=CONVERSATION_ID)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.listen_conversation(conversation_id=CONVERSATION_ID)
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
