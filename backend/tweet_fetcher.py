import snscrape.modules.twitter as sntwitter

def fetch_tweets(query, limit=5):
    tweets = []
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            tweets.append(tweet.content)
    except:
        pass
    return tweets
