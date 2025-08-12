# backend/news_fetcher.py
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from datetime import datetime, timedelta


def fetch_google_news_for_symbol(symbol: str, top_n: int = 5) -> List[Dict]:
    """
    Fetch Google News RSS results for a stock symbol or keyword.
    Returns: List[Dict] with keys 'title', 'link', 'snippet'.
    """
    if not symbol:
        return []

    query = quote_plus(symbol)
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; spike-finder/1.0)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception:
        return []

    items = []
    soup = BeautifulSoup(r.content, "xml")
    for item in soup.find_all("item")[:top_n]:
        title = item.title.text if item.title else ""
        link = item.link.text if item.link else ""
        description = item.description.text if item.description else ""
        items.append({"title": title, "link": link, "snippet": description})
    return items


def fetch_news(stock_name, api_key="YOUR_NEWS_API_KEY"):
    """
    Fetch recent news about a stock using NewsAPI.
    Requires an API key from https://newsapi.org/
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": stock_name,
        "from": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "sortBy": "relevancy",
        "apiKey": api_key,
        "language": "en"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching news: {response.status_code}")
    return response.json().get("articles", [])
