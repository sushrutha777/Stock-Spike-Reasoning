import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta

def fetch_tweets(query: str, hours=6, limit=10):
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f"{query} lang:en").get_items():
        if tweet.date < cutoff:
            break
        tweets.append(tweet.content)
        if len(tweets) >= limit:
            break
    return tweets
