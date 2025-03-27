from typing import List, Dict
import streamlit as st

class MessageManager:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def add_message(self, role: str, content: str):
        """Add a new message to the session state."""
        st.session_state.messages.append({"role": role, "content": content})

    def display_messages(self):
        """Display all messages in the chat."""
        chat_html = "<div class='chat-container'>"
        for message in st.session_state.messages:
            if message["role"] == "user":
                chat_html += f"<div class='user-message'>{message['content']}</div>"
            else:
                chat_html += f"<div class='bot-message'>{message['content']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
