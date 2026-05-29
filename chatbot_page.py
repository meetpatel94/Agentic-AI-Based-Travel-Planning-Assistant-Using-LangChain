import streamlit as st
from chatbot import ask_chatbot

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Travel Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# TITLE
# ==========================================

st.title("🤖 AI Travel Chatbot")

st.write("Ask anything about travel")

st.divider()

# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# ==========================================
# SHOW OLD MESSAGES
# ==========================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

# ==========================================
# USER INPUT
# ==========================================

user_input = st.chat_input(
    "Ask your travel question..."
)

# ==========================================
# CHATBOT RESPONSE
# ==========================================

if user_input:

    st.session_state.messages.append({

        "role": "user",

        "content": user_input
    })

    with st.chat_message("user"):

        st.write(user_input)

    bot_response = ask_chatbot(user_input)

    st.session_state.messages.append({

        "role": "assistant",

        "content": bot_response
    })

    with st.chat_message("assistant"):

        st.write(bot_response)