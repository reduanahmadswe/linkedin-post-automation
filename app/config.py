import os
from dotenv import load_dotenv

# Load .env file FIRST before any os.getenv() calls
load_dotenv()

def load_env():
    """Reload environment variables if needed (e.g., after .env file changes)"""
    load_dotenv(override=True)

# API Keys
GEMINI_KEYS = os.getenv("GEMINI_KEYS", "").split(",")
OPENROUTER_KEYS = os.getenv("OPENROUTER_KEYS", "").split(",")
OPENAI_KEYS = os.getenv("OPENAI_KEYS", "").split(",")

# LinkedIn credentials
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")
