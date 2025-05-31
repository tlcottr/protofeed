# formatter.py

from rich import print
from rich.table import Table

def display_table(posts):
    table = Table(title="ProtoFeed Results")

    table.add_column("Post", style="cyan", no_wrap=False)
    table.add_column("Score", justify="right")
    table.add_column("Sentiment")
    table.add_column("Category")

    for post in posts:
        title = post["title"][:60] + ("..." if len(post["title"]) > 60 else "")
        table.add_row(
            title,
            str(post["score"]),
            post.get("sentiment", "–"),
            post.get("category", "–")
        )

    print(table)
