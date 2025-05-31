# x_fetcher.py

import snscrape.modules.twitter as sntwitter

def fetch_tweets(brand, limit=10):
    query = f'"{brand}" lang:en since:2023-01-01'
    tweets = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        tweets.append({
            "title": tweet.content,
            "score": tweet.likeCount,
            "url": tweet.url,
            "platform": "x"
        })

    return tweets
