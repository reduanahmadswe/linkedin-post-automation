import os
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TOPICS = [
    "Artificial Intelligence (AI)",
    "Software Engineering",
    "Web Development",
    "Programming",
    "Backend Development",
    "Frontend Development",
    "System Design",
    "DevOps",
    "Open Source",
    "Developer Productivity",
    "Coding Best Practices",
    "Learning Programming",
    "Career Growth in Tech",
    "Startup / Tech mindset"
]

STYLE_PROMPT = """You are a professional LinkedIn content generator integrated into an automated posting system.

Your job is to generate short LinkedIn posts in Bengali related to technology.

POST RULES

1. Write in Bengali language.
2. Keep the post short (50 to 120 words).
3. Use LinkedIn style formatting.
4. Use small paragraphs.
5. Optionally include 2 to 4 bullet points.
6. Start with a strong hook question or statement.
7. End with a simple question or call-to-action.
8. Each generated post must be about a different idea.

IMPORTANT FORMAT RULE

Do NOT use the long dash character "—".

Instead use:

* normal dash "-"
* bullet points
* or line breaks.

POST STYLE

Hook
Short explanation
Optional bullet points
Call to action

Example style:

👨‍💻 অনেকেই programming শেখে, কিন্তু debugging শেখে না।

একজন ভালো software engineer হওয়ার জন্য শুধু code লিখলেই হয় না।

গুরুত্বপূর্ণ কিছু বিষয়:

* clean code
* problem solving
* system thinking

আপনার coding শেখার সময় সবচেয়ে বড় challenge কী?

Now generate ONE new unique LinkedIn post.
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
        model="gpt-4o-mini",
        input=prompt,
        store=True,
    )
    print("OpenAI response:", response)
    return response.output_text, topic
