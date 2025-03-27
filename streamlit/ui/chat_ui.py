import streamlit as st
from services.backend_request_strategy import BackendQueryRequest
from services.chat_service import ChatService
from services.message_manager import MessageManager


def chat_ui():
    # Setup dependencies
    backend_request_strategy = BackendQueryRequest()
    chat_service = ChatService(backend_request_strategy)
    message_manager = MessageManager()

    # Streamlit UI Setup
    st.markdown("""
        <style>
        /* Global styles */
        body {
            font-family: 'Inter', sans-serif;
        }
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 20px;
        }
        .user-message {
            background-color: #3b82f6;
            color: white;
            padding: 12px 16px;
            border-radius: 12px;
            margin: 8px 0;
            max-width: 70%;
            float: right;
            clear: both;
        }
        .bot-message {
            background-color: #e5e7eb;
            color: #1f2937;
            padding: 12px 16px;
            border-radius: 12px;
            margin: 8px 0;
            max-width: 70%;
            float: left;
            clear: both;
        }
        .input-container {
            display: flex;
            gap: 10px;
            padding: 10px;
            background-color: #ffffff;
        }
        .stTextInput > div > div > input {
            border: none;
            border-radius: 8px;
            padding: 10px;
            background-color: #f3f4f6;
            color: #000000;
        }
        .stButton > button {
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>FinWhiz</h1>", unsafe_allow_html=True)

    with st.container():
        chat_container = st.empty()

    with st.form(key="query_form", clear_on_submit=True):
        query = st.text_input("Type your query:", placeholder="e.g., What was my biggest expense this month?")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and query:
        # Add user message
        message_manager.add_message("user", query)
        
        # Get bot response
        bot_response = chat_service.get_response(query)
        
        # Add bot message
        message_manager.add_message("bot", bot_response)

        # Display all messages
        message_manager.display_messages()

    if not submit_button:
        message_manager.display_messages()
