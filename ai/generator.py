import os
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TOPICS = [
    "programming",
    "backend development",
    "learning programming",
    "developer mindset",
    "AI tools",
    "career advice",
    "software engineering practices"
]

STYLE_PROMPT = """
Generate a LinkedIn post in Bengali, motivational, short paragraphs, emojis, bullet points, programming topics, career advice, software engineering thoughts. 150-250 words.
"""

# Load OpenAI key from environment variable
OPENAI_KEY = os.getenv("OPENAI_KEY", "")
if not OPENAI_KEY:
    raise ValueError("OPENAI_KEY environment variable is not set!")

client = OpenAI(api_key=OPENAI_KEY)

def generate_post():
    topic = random.choice(TOPICS)
    prompt = f"{STYLE_PROMPT}\nTopic: {topic}"
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
        store=True,
    )
    print("OpenAI response:", response)
    return response.output_text, topic
