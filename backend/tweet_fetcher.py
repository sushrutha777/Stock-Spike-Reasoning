# backend/tweet_fetcher.py
"""
Tweet Fetcher
-------------
Fetches recent tweets for a given stock keyword using snscrape.
No Twitter API keys needed.
"""

import snscrape.modules.twitter as sntwitter
from typing import List
import datetime

def fetch_tweets_by_query(query: str, limit: int = 20) -> List[str]:
    """
    Fetch recent tweets containing the query keyword.

    Args:
        query (str): The search keyword (e.g., stock name or ticker).
        limit (int): Maximum number of tweets to fetch.

    Returns:
        List[str]: A list of tweet texts.
    """
    tweets = []
    since_date = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    search_query = f"{query} since:{since_date} lang:en"

    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
            if i >= limit:
                break
            tweets.append(tweet.content)
    except Exception as e:
        print(f"[Error] Could not fetch tweets: {e}")

    return tweets


if __name__ == "__main__":
    test = fetch_tweets_by_query("Zomato", limit=5)
    print(test)
