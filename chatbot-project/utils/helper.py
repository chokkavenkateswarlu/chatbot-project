import logging
from datetime import datetime
import streamlit as st

def setup_logging():
    """
    Set up logging configuration
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('chatbot.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def format_timestamp(timestamp=None):
    """
    Format timestamp for display
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%H:%M:%S")

def format_message(message, is_user=False):
    """
    Format message for display
    """
    timestamp = format_timestamp()
    prefix = "You" if is_user else "Bot"
    return f"{timestamp} - {prefix}: {message}"

def validate_api_key(api_key):
    """
    Validate DeepSeek API key format
    """
    if not api_key or api_key == "your_deepseek_api_key_here":
        return False
    return len(api_key) > 20  # Basic validation

logger = setup_logging()