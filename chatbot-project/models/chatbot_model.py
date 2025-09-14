import requests
import json
from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL

def generate_deepseek_response(messages, max_tokens=500, temperature=0.7):
    """
    Generate response using DeepSeek AI API
    """
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling DeepSeek API: {e}")
        return "I'm having trouble connecting to my AI service. Please try again later."
    except KeyError as e:
        print(f"Error parsing DeepSeek response: {e}")
        return "I encountered an issue processing the response. Please try again."

def create_chat_message(role, content):
    """
    Create a message object for the chat API
    """
    return {"role": role, "content": content}