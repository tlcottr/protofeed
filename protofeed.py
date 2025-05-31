from reddit_fetcher import fetch_posts
from formatter import display_table
from exporter import export_csv, export_markdown  # ← NEW
from analyzer import analyze_post, summarize_posts


def run_protofeed(brand: str):
    print(f"\n[bold yellow]Fetching posts for:[/] [bold green]{brand}[/]\n")
    posts = fetch_posts(brand)

    for post in posts:
        print(f"Analyzing: {post['title'][:50]}...")
        analysis = analyze_post(post["title"])
        post.update(analysis)

    display_table(posts)
    summary = summarize_posts(posts, brand)
    print(f"\n[bold blue]🧠 Summary:[/bold blue]\n{summary}\n")
    
    export_csv(posts, brand)
    export_markdown(posts, brand, summary)  # updated function next

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("[red]Usage: python protofeed.py [brand][/red]")
    else:
        run_protofeed(sys.argv[1])