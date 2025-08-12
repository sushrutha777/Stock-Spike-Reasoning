# __init__.py
"""
Backend package for Stock Spike Reason Finder
Contains:
- spike_detector: logic to detect price spikes
- news_fetcher: fetches related news
- summarizer: summarizes text
- tweet_fetcher: fetches recent tweets
- nse_fetcher: gets NSE stock data
"""

from .spike_detector import detect_spikes
from .summarizer import summarize_text
from .nse_fetcher import get_nse_stocks

__all__ = [
    "detect_spikes",
    "summarize_text",
    "get_nse_stocks"
]