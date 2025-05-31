# api/index.py

from flask import Flask, request, render_template
from reddit_fetcher import fetch_posts
from x_fetcher import fetch_tweets
from analyzer import analyze_post, summarize_posts

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        brand = request.form["brand"]

        # Fetch posts from both Reddit and X
        reddit_posts = fetch_posts(brand)
        x_posts = fetch_tweets(brand)

        # Combine and analyze
        all_posts = reddit_posts + x_posts
        for post in all_posts:
            analysis = analyze_post(post["title"])
            post.update(analysis)

        summary = summarize_posts(all_posts, brand)

        return render_template("index.html", posts=all_posts, summary=summary, brand=brand)

    return render_template("index.html", posts=None)
