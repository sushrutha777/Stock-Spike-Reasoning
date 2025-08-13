import requests
from bs4 import BeautifulSoup

def fetch_google_news(stock):
    try:
        query = stock.replace(" ", "+")
        url = f"https://news.google.com/rss/search?q={query}+stock"
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.content, features="xml")
        headlines = [item.title.text for item in soup.find_all("item")][:5]
        return headlines
    except:
        return []
