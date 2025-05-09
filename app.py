from client import BotpressClient
import streamlit as st
from constants import CONVERSATION_ID

st.title("Botpress Front-end for Streamlit")

client = BotpressClient(
    api_id=st.secrets["CHAT_API_ID"], user_key=st.secrets["USER_KEY"]
)

if "messages" not in st.session_state:
    messages = client.list_messages(CONVERSATION_ID)
    next_token = messages["meta"]["nextToken"]
    st.session_state.messages = messages["messages"][::-1]

for message in st.session_state.messages:
    with st.chat_message(message["userId"]):
        st.markdown(message["payload"]["text"])

if prompt := st.chat_input("*wine*-d it up"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    client.create_message(prompt, conversation_id=CONVERSATION_ID)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.listen_conversation(conversation_id=CONVERSATION_ID)
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
