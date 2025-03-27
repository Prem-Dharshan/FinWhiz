import streamlit as st
from ui.chat_ui import chat_ui

# Setup the page configuration
st.set_page_config(
    page_title="FinWhiz",
    page_icon="💰",
    layout="wide"
)

# Display the chat interface UI
chat_ui()
