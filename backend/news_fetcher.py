import feedparser
from datetime import datetime, timedelta

def fetch_news(query: str, hours=6):
    feed_url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(feed_url)
    
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    articles = []
    
    for entry in feed.entries:
        pub_date = datetime(*entry.published_parsed[:6])
        if pub_date > cutoff:
            articles.append({
                "title": entry.title,
                "link": entry.link
            })
    return articles
