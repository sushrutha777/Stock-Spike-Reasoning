# backend/tweet_fetcher.py
# uses snscrape (no Twitter API required)
import subprocess
import sys
import json
from datetime import datetime, timedelta


def fetch_tweets_by_query(query: str, max_tweets: int = 50):
    """Fetch tweets using snscrape via subprocess and return a list of dicts.

    snscrape must be installed (pip install snscrape), and this runs the command-line scraper.
    """
    # Construct command
    cmd = [
        sys.executable, "-m", "snscrape.modules.twitter", "TwitterSearch",
        f"{query}", "--max-results", str(max_tweets), "--jsonl"
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            return []
        lines = proc.stdout.strip().splitlines()
        tweets = [json.loads(line) for line in lines if line.strip()]
        # Simplify tweet objects
        simplified = []
        for t in tweets:
            simplified.append({
                'date': t.get('date'),
                'content': t.get('content'),
                'user': t.get('user', {}).get('username') if t.get('user') else None,
                'url': t.get('url')
            })
        return simplified
    except Exception as e:
        print("snscrape error:", e)
        return []


if __name__ == "__main__":
    q = "Infosys"
    print(fetch_tweets_by_query(q, max_tweets=10))