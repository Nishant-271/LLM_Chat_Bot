import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


# Configure Gemini
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Use the correct model name
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Function to translate roles
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Page config
st.set_page_config(page_title="Chat with Nish-Astra.AI PRO ⚔️", page_icon="🐙", layout="centered")

# Custom CSS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f0f4ff, #e3f6fc);
    }

    .chat-title {
        font-size: 2.7rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
            
        margin-bottom: 1rem;
        border-radius: 1rem;
        background: linear-gradient(to right, #fefcea, #f1daff);
        color: #1a1a40;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        background-color: #ffffffcc;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .chat-message.user {
        background: linear-gradient(to right, #c0f7ff, #e0ffe6);
        align-self: flex-end;
    }

    .chat-message.assistant {
   background: linear-gradient(to left, #fefcea, #f1daff);;
        align-self: flex-start;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="chat-title"> 🐙 NishAstra – Your AI Companion!</div>', unsafe_allow_html=True)

# Chat history display
for message in st.session_state.chat_session.history:
    role_class = translate_role_for_streamlit(message.role)
    with st.chat_message(role_class):
        st.markdown(f'<div class="chat-message {role_class}">{message.parts[0].text}</div>', unsafe_allow_html=True)

# User input section
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    st.chat_message("user").markdown(f'<div class="chat-message user">{user_prompt}</div>', unsafe_allow_html=True)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant"):
        st.markdown(f'<div class="chat-message assistant">{gemini_response.text}</div>', unsafe_allow_html=True)
