# exporter.py

import csv
import os

def export_csv(posts, brand):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{brand}_report.csv"
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "score", "sentiment", "category"])
        writer.writeheader()
        for post in posts:
            writer.writerow({
                "title": post["title"],
                "score": post["score"],
                "sentiment": post["sentiment"],
                "category": post["category"]
            })
    print(f"\n[green]✔ Exported CSV to {filepath}[/green]")

def export_markdown(posts, brand, summary=None):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{brand}_summary.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# ProtoFeed Summary: {brand}\n\n")
        if summary:
            f.write(f"> {summary}\n\n---\n\n")
        for post in posts:
            f.write(f"**Post:** {post['title']}\n\n")
            f.write(f"- Sentiment: {post['sentiment']}\n")
            f.write(f"- Category: {post['category']}\n")
            f.write(f"- Score: {post['score']}\n\n---\n\n")
    print(f"[green]✔ Exported Markdown with summary to {filepath}[/green]")

