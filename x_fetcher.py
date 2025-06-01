# x_fetcher.py

import requests
import os

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")  # Store this in your .env or shell

def fetch_x_posts(brand, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    query_params = {
        'query': f'{brand} lang:en -is:retweet',
        'max_results': str(max_results),
        'tweet.fields': 'created_at,public_metrics,author_id',
    }

    response = requests.get(search_url, headers=headers, params=query_params)

    if response.status_code != 200:
        raise Exception(f"X API error: {response.status_code} - {response.text}")

    tweets = response.json().get("data", [])
    formatted = []

    for tweet in tweets:
        formatted.append({
            "title": tweet["text"],
            "score": tweet["public_metrics"]["like_count"],
            "source": "X",
            "timestamp": tweet["created_at"]
        })

    return formatted
