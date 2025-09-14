import sys

print("Python version:", sys.version)
print("\nTesting imports...")

libs = [
    "streamlit", "requests", "faiss", "sentence_transformers", 
    "nltk", "sqlalchemy", "dotenv", "speech_recognition", 
    "gtts", "pygame", "torch"
]

for lib in libs:
    try:
        __import__(lib)
        print(f"✓ {lib} imported successfully")
    except ImportError as e:
        print(f"✗ {lib} failed: {e}")