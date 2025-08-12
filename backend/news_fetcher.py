# backend/news_fetcher.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def fetch_google_news_for_symbol(symbol: str, top_n=5):
    """Fetch Google News RSS search results for a symbol or keyword.

    Uses the free Google News RSS endpoint:
    https://news.google.com/rss/search?q=<query>

    Returns a list of dicts: {title, link, snippet}
    """
    query = quote(symbol)
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    r = requests.get(url, timeout=10)
    items = []
    if r.status_code != 200:
        return items
    soup = BeautifulSoup(r.content, "xml")
    for i, item in enumerate(soup.find_all('item')[:top_n]):
        title = item.title.text if item.title else ""
        link = item.link.text if item.link else ""
        description = item.description.text if item.description else ""
        items.append({"title": title, "link": link, "snippet": description})
    return items


if __name__ == "__main__":
    print(fetch_google_news_for_symbol("Infosys"))