# api/index.py

from flask import Flask, request, render_template
from reddit_fetcher import fetch_posts
from analyzer import analyze_post, summarize_posts
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        brand = request.form["brand"]

        posts = fetch_posts(brand)

        for post in posts:
            analysis = analyze_post(post["title"])
            post.update(analysis)

        summary = summarize_posts(posts, brand)

        return render_template("index.html", posts=posts, summary=summary, brand=brand)

    return render_template("index.html", posts=[], brand="", summary=None)


