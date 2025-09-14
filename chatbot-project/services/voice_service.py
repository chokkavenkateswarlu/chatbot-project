import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import tempfile
import os
from config.settings import ENABLE_VOICE

def speech_to_text():
    """
    Convert speech to text using microphone input
    """
    if not ENABLE_VOICE:
        return None
    
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Error with speech recognition service: {e}")
        return None

def text_to_speech(text, lang='en'):
    """
    Convert text to speech and play it
    """
    if not ENABLE_VOICE:
        return
    
    try:
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(tmpfile.name)
            
            # Initialize pygame mixer and play audio
            pygame.mixer.init()
            pygame.mixer.music.load(tmpfile.name)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.quit()
            os.unlink(tmpfile.name)
            
    except Exception as e:
        print(f"Error in text-to-speech: {e}")