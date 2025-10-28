import os
import streamlit as st
import google.generativeai as genai
import traceback

# ---------------------------
# STREAMLIT + GOOGLE API SETUP
# ---------------------------

st.set_page_config(
    page_title="Chat with Nish-Astra.AI PRO ⚔️",
    page_icon="🐙",
    layout="centered"
)

# Get Google API Key safely from Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
else:
    st.error("❌ GOOGLE_API_KEY not found in Streamlit Secrets.")
    st.stop()

# ---------------------------
# INITIALIZE MODEL
# ---------------------------

try:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
 
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def translate_role_for_streamlit(user_role):
    """Converts Gemini role to Streamlit-friendly name."""
    return "assistant" if user_role == "model" else user_role

# Initialize chat session if not already in session state
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"❌ Failed to start chat session: {e}")
        st.stop()

# ---------------------------
# STYLING
# ---------------------------

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
    background: linear-gradient(to left, #fefcea, #f1daff);
    align-self: flex-start;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# UI: TITLE + CHAT HISTORY
# ---------------------------

st.markdown('<div class="chat-title"> 🐙 NishAstra – Your AI Companion!</div>', unsafe_allow_html=True)

for message in st.session_state.chat_session.history:
    role_class = translate_role_for_streamlit(message.role)
    with st.chat_message(role_class):
        st.markdown(
            f'<div class="chat-message {role_class}">{message.parts[0].text}</div>',
            unsafe_allow_html=True
        )

# ---------------------------
# CHAT INPUT HANDLING
# ---------------------------

user_prompt = st.chat_input("Ask NishAstra (Gemini-1.5-Flash)...")

if user_prompt:
    # Display user message immediately
    st.chat_message("user").markdown(
        f'<div class="chat-message user">{user_prompt}</div>', unsafe_allow_html=True
    )

    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(
                f'<div class="chat-message assistant">{gemini_response.text}</div>',
                unsafe_allow_html=True
            )
    except Exception as e:
        st.error("⚠️ Error while communicating with Gemini API.")
        st.code(traceback.format_exc())
