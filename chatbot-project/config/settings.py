import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DeepSeek AI Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your_deepseek_api_key_here")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# Knowledge Base Configuration
KNOWLEDGE_BASE_PATH = "data/knowledge_base.txt"
INTENTS_PATH = "data/intents.json"

# Database Configuration
DB_PATH = "data/chat_history.db"

# NLP Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.7  # Threshold for FAQ matching

# Voice Configuration (Optional)
ENABLE_VOICE = False