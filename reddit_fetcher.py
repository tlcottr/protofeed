# reddit_fetcher.py

import os
from datetime import datetime, timedelta
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT", "protofeed")
)

def fetch_posts(brand: str, limit: int = 10):
    posts = []
    for submission in reddit.subreddit("all").search(brand, sort="new", limit=limit):
        if submission.created_utc > (datetime.utcnow() - timedelta(days=1)).timestamp():
            posts.append({
                "title": submission.title,
                "score": submission.score,
                "url": submission.url
            })
    return posts
