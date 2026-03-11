from app.config import GEMINI_KEYS, OPENROUTER_KEYS, OPENAI_KEYS

KEYS = {
    "gemini": GEMINI_KEYS,
    "openrouter": OPENROUTER_KEYS,
    "openai": OPENAI_KEYS
}

def get_next_key(provider):
    for key in KEYS.get(provider, []):
        yield key
