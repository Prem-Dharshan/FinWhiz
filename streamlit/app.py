import streamlit as st
import requests

# Custom CSS for a modern Shadcn-inspired design
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
        /* No explicit background or border, blends with Streamlit's default */
    }
    .user-message {
        background-color: #3b82f6; /* Blue for user */
        color: white;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .bot-message {
        background-color: #e5e7eb; /* Gray for bot */
        color: #1f2937;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .input-container {
        display: flex;
        gap: 10px;
        padding: 10px;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stTextInput > div > div > input {
        border: none;
        border-radius: 8px;
        padding: 10px;
        background-color: #f3f4f6;
        color: #000000; /* Set input text color to black */
        width: 100%;
    }
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #2563eb;
    }
    </style>
""", unsafe_allow_html=True)

# Set up the title with white color
st.markdown("<h1 style='text-align: center; color: #ffffff;'>FinWhiz</h1>", unsafe_allow_html=True)

# Create a container for the chat messages
with st.container():
    chat_container = st.empty()  # Use empty container to update dynamically

# Store the messages history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to display messages
def display_messages():
    chat_html = "<div class='chat-container'>"
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_html += f"<div class='user-message'>{message['content']}</div>"
        else:
            chat_html += f"<div class='bot-message'>{message['content']}</div>"
    chat_html += "</div>"
    chat_container.markdown(chat_html, unsafe_allow_html=True)

# Input form at the bottom
with st.form(key="query_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Type your query:", placeholder="e.g., What was my biggest expense this month?", label_visibility="collapsed")
    with col2:
        submit_button = st.form_submit_button(label="Send")

# Handle form submission
if submit_button and query:
    # Add user query to the chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Send the query to the backend service
    try:
        response = requests.post("http://backend:8000/query", json={"query": query})
        response.raise_for_status()
        
        # Extract the response
        response_data = response.json()
        bot_response = response_data.get("response", "Sorry, I didn't understand that.")
        
        # Add bot response to the chat history
        st.session_state.messages.append({"role": "bot", "content": bot_response})

    except requests.exceptions.RequestException as e:
        st.session_state.messages.append({"role": "bot", "content": f"Error: {str(e)}"})

    # Update the chat display
    display_messages()

# Initial display of messages (only on page load)
if not submit_button:
    display_messages()