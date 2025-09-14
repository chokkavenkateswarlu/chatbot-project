import sqlite3
import json
from datetime import datetime
from config.settings import DB_PATH

def init_db():
    """
    Initialize the database
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create conversations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        session_id TEXT,
        timestamp DATETIME,
        role TEXT,
        message TEXT,
        PRIMARY KEY (session_id, timestamp)
    )
    ''')
    
    conn.commit()
    conn.close()

def save_message(session_id, role, message):
    """
    Save a message to the database
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO conversations (session_id, timestamp, role, message) VALUES (?, ?, ?, ?)",
        (session_id, timestamp, role, message)
    )
    
    conn.commit()
    conn.close()

def get_conversation_history(session_id, limit=20):
    """
    Retrieve conversation history for a session
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT role, message, timestamp FROM conversations WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
        (session_id, limit)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    # Format as list of messages
    history = [{"role": "user" if row[0] == "user" else "assistant", "content": row[1]} for row in reversed(rows)]
    return history

def clear_conversation_history(session_id):
    """
    Clear conversation history for a session
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM conversations WHERE session_id = ?",
        (session_id,)
    )
    
    conn.commit()
    conn.close()

# Initialize database on import
init_db()