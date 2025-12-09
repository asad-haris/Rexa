# utils.py
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def clean_text(text: str) -> str:
    """
    Clean and preprocess text for better similarity matching.

    Steps:
    - Convert to lowercase
    - Remove extra spaces
    - Remove special characters (optional for better matching)
    """
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'[^a-z0-9\s.,]', '', text)  # Remove unwanted characters but keep basic punctuation
    return text

def get_openai_key() -> str:
    """
    Retrieve the OpenAI API key from environment variables.
    Returns:
        str: OpenAI API key or None if not found.
    """
    return os.getenv("OPENAI_API_KEY")
