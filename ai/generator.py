import os
import random
import logging
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)

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

HUMANIZED_PROMPT = """আপনি একজন বাংলাদেশি software developer যিনি LinkedIn-এ নিজের coding experience শেয়ার করেন।

আপনার কাজ হলো Bengali-তে একটা ছোট LinkedIn post লেখা - যেটা পড়লে মনে হবে একজন real developer লিখেছেন, কোনো AI না।

POST RULES

1. সম্পূর্ণ Bengali-তে লিখবেন (technical terms English-এ রাখতে পারেন)
2. 50-120 words এর মধ্যে রাখবেন
3. ছোট ছোট paragraph ব্যবহার করবেন
4. প্রয়োজনে 2-4টা bullet point দিতে পারেন
5. শুরুতে একটা relatable hook দেবেন
6. শেষে simple question বা thought দিয়ে end করবেন

WRITING STYLE - এটা সবচেয়ে গুরুত্বপূর্ণ

- Professional কিন্তু friendly tone রাখবেন
- Personal experience বা observation শেয়ার করবেন
- Simple words ব্যবহার করবেন
- AI-এর মতো perfect বা robotic শোনাবে না
- Repetitive phrases avoid করবেন

LANGUAGE RULES - অবশ্যই মানতে হবে

- সবসময় "আপনি", "আপনার", "আপনাদের" ব্যবহার করবেন
- কখনোই "তুমি", "তোমার", "তুই", "তোর" ব্যবহার করবেন না
- Reader-কে সম্মানজনক ভাবে address করবেন

FORBIDDEN

- Long dash "—" একদম ব্যবহার করবেন না
- "এই পোস্টে", "আজকে আমরা", "চলুন জানি" এসব avoid করবেন
- অতিরিক্ত emoji দেবেন না (max 1-2)
- Generic motivational lines দেবেন না
- "তুমি", "তোমার", "তুই", "তোর" একদম ব্যবহার করবেন না

EXAMPLE TONES (এরকম natural sound করবে)

"আজ coding করতে গিয়ে একটা জিনিস বুঝলাম..."

"Programming শেখার সময় একটা mistake অনেকেই করেন..."

"গতকাল একটা bug fix করতে গিয়ে 3 ঘণ্টা গেল..."

"অনেকে জিজ্ঞেস করেন কোন language দিয়ে শুরু করব..."

"আপনার কি কখনো এমন হয়েছে যে..."

POST FORMAT

Hook (relatable situation বা question)
Short explanation (নিজের experience/insight)
Optional bullet points
Ending thought বা question (আপনি দিয়ে address করবেন)

Now generate ONE unique LinkedIn post about the given topic. Make it sound like a real developer sharing a genuine thought. Remember: ALWAYS use আপনি, NEVER use তুমি/তুই.
"""

# Load OpenAI key from environment variable
OPENAI_KEY = os.getenv("OPENAI_KEY", "")
if not OPENAI_KEY:
    raise ValueError("OPENAI_KEY environment variable is not set!")

client = OpenAI(api_key=OPENAI_KEY)


def generate_post() -> str:
    """
    Generate a humanized LinkedIn post in Bengali.
    Returns the post content ready to publish.
    """
    topic = random.choice(TOPICS)
    prompt = f"{HUMANIZED_PROMPT}\nTopic: {topic}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Bengali software developer writing authentic LinkedIn posts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        top_p=0.9,
        max_tokens=500
    )
    
    post_content = response.choices[0].message.content.strip()
    
    # Replace any long dashes that might have slipped through
    post_content = post_content.replace("—", "-")
    post_content = post_content.replace("–", "-")
    
    logger.info("Generated humanized LinkedIn post")
    logger.debug(f"Topic: {topic}")
    
    return post_content
