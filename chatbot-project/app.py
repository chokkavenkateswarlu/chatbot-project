import streamlit as st
import time
import uuid
import os
from datetime import datetime

# Import project modules
from config.settings import DEEPSEEK_API_KEY
from models.chatbot_model import generate_deepseek_response, create_chat_message
from services.retrieval_service import knowledge_base
from services.voice_service import speech_to_text, text_to_speech
from utils.database import save_message, get_conversation_history, clear_conversation_history
from utils.helper import validate_api_key, logger, format_timestamp

# Page configuration
st.set_page_config(
    page_title="DeepSeek Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("static/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = DEEPSEEK_API_KEY

# Sidebar for settings
with st.sidebar:
    # ✅ Safe path for image
    image_path = os.path.join("static", "bot_avatar.png")  # change filename if needed
    if os.path.exists(image_path):
        st.image(image_path, width=100)
    else:
        st.warning("⚠️ Bot avatar image not found in static/ folder.")
    
    st.title("Chatbot Settings")
    
    # API key input
    api_key = st.text_input("DeepSeek API Key", value=st.session_state.api_key, type="password")
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.success("API key updated!")
    
    # Voice settings
    voice_enabled = st.checkbox("Enable Voice", value=False)
    
    # Clear chat button
    if st.button("Clear Conversation"):
        clear_conversation_history(st.session_state.session_id)
        st.session_state.messages = []
        st.rerun()
    
    # Display conversation history
    st.subheader("Conversation History")
    history = get_conversation_history(st.session_state.session_id)
    for msg in history:
        st.text(f"{msg['role']}: {msg['content']}")

# Main chat interface
st.title("🤖 DeepSeek Chatbot")
st.markdown("Chat with our AI assistant powered by DeepSeek AI")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice input button
if voice_enabled:
    if st.button("🎤 Voice Input"):
        with st.spinner("Listening..."):
            voice_text = speech_to_text()
            if voice_text:
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": voice_text})
                save_message(st.session_state.session_id, "user", voice_text)
                
                with st.chat_message("user"):
                    st.markdown(voice_text)
                
                # Generate response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        kb_response = knowledge_base.get_best_match(voice_text)
                        
                        if kb_response:
                            response = kb_response
                            st.markdown(response)
                            if voice_enabled:
                                text_to_speech(response)
                        else:
                            conversation_history = [
                                create_chat_message("system", "You are a helpful AI assistant.")
                            ]
                            for msg in st.session_state.messages[-6:]:
                                role = "user" if msg["role"] == "user" else "assistant"
                                conversation_history.append(create_chat_message(role, msg["content"]))
                            
                            if validate_api_key(st.session_state.api_key):
                                response = generate_deepseek_response(conversation_history)
                            else:
                                response = "Please provide a valid DeepSeek API key in the settings."
                            
                            st.markdown(response)
                            if voice_enabled:
                                text_to_speech(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                save_message(st.session_state.session_id, "assistant", response)

# Text input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.session_id, "user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            kb_response = knowledge_base.get_best_match(prompt)
            
            if kb_response:
                response = kb_response
                st.markdown(response)
                if voice_enabled:
                    text_to_speech(response)
            else:
                conversation_history = [
                    create_chat_message("system", "You are a helpful AI assistant.")
                ]
                for msg in st.session_state.messages[-6:]:
                    role = "user" if msg["role"] == "user" else "assistant"
                    conversation_history.append(create_chat_message(role, msg["content"]))
                
                if validate_api_key(st.session_state.api_key):
                    response = generate_deepseek_response(conversation_history)
                else:
                    response = "Please provide a valid DeepSeek API key in the settings."
                
                st.markdown(response)
                if voice_enabled:
                    text_to_speech(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_message(st.session_state.session_id, "assistant", response)

# Footer
st.markdown("---")
st.markdown("Powered by [DeepSeek AI](https://www.deepseek.com/) | Built with Streamlit")
