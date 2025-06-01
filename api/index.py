from flask import Flask, request, render_template, send_file
from reddit_fetcher import fetch_posts
from x_fetcher import fetch_x_posts
from analyzer import analyze_post, summarize_posts, generate_gpt_insight
import sys
import os
import datetime
import csv
from collections import Counter

# Ensure parent directory is on the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

LOG_FILE = "logs.txt"

def log_query(brand):
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp}, {brand}\n")

def read_brand_counts():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        brands = [line.strip().split(", ")[1] for line in f.readlines() if ", " in line]
        return Counter(brands).most_common(10)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        brand = request.form["brand"]
        log_query(brand)

        # Fetch posts from Reddit
        reddit_posts = fetch_posts(brand)
        for post in reddit_posts:
            analysis = analyze_post(post["title"])
            post.update(analysis)
            post["source"] = "Reddit"

        # Fetch posts from X (Twitter)
        try:
            x_posts = fetch_x_posts(brand)
            for post in x_posts:
                analysis = analyze_post(post["title"])
                post.update(analysis)
                post["source"] = "X"
        except Exception as e:
            x_posts = []
            print(f"X Fetch Error: {e}")

        # Merge sources
        all_posts = reddit_posts + x_posts

        # Summarize and generate GPT insight
        summary = summarize_posts(all_posts, brand)
        gpt_summary = generate_gpt_insight(all_posts, brand)

        return render_template("index.html", posts=all_posts, summary=summary, gpt_summary=gpt_summary, brand=brand)

    return render_template("index.html", posts=[], brand="", summary=None, gpt_summary=None)


@app.route("/analytics")
def analytics():
    top_brands = read_brand_counts()
    labels = [brand for brand, _ in top_brands]
    counts = [count for _, count in top_brands]
    return render_template("analytics.html", labels=labels, counts=counts)

@app.route("/export")
def export_logs():
    if not os.path.exists(LOG_FILE):
        return "No logs found.", 404
    export_file = "query_logs.csv"
    with open(LOG_FILE, "r") as infile, open(export_file, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Timestamp", "Brand"])
        for line in infile:
            if ", " in line:
                writer.writerow(line.strip().split(", "))
    return send_file(export_file, as_attachment=True)

