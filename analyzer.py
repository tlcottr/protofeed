# analyzer.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_post(text: str) -> dict:
    prompt = f"""
You are a brand analyst. Categorize the sentiment and type of the following social post.

Post: "{text}"

Return:
Sentiment: Positive / Neutral / Negative
Category: Product Hype, Complaint, Meme, Drop Alert, Customer Experience, Other
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()
    lines = content.split("\n")
    sentiment = lines[0].split(":")[1].strip()
    category = lines[1].split(":")[1].strip()
    return {"sentiment": sentiment, "category": category}

def summarize_posts(posts, brand: str) -> str:
    bullet_list = "\n".join([
        f"- {p['title']} (Sentiment: {p['sentiment']}, Category: {p['category']})"
        for p in posts
    ])

    prompt = f"""
You're a brand strategist reviewing social chatter about {brand}. Here's a list of 10 recent Reddit posts and how they were classified:

{bullet_list}

Write a 3-4 sentence summary highlighting the emotional tone, trends, and anything the brand team should pay attention to.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
