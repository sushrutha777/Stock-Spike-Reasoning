# backend/nse_fetcher.py
"""
NSE Stock Fetcher using Yahoo Finance
"""

import yfinance as yf
from typing import List, Optional


def fetch_nse_quote(symbol: str) -> Optional[float]:
    """
    Fetch the latest NSE stock price using Yahoo Finance.
    """
    try:
        ticker = yf.Ticker(symbol + ".NS")
        data = ticker.history(period="1d")
        if not data.empty:
            return round(data["Close"].iloc[-1], 2)
    except Exception as e:
        print(f"[Error] Could not fetch NSE quote for {symbol}: {e}")
    return None


def get_nse_stocks() -> List[str]:
    """
    Return a sample list of popular NSE stock symbols.
    You can replace this with a database or API fetch later.
    """
    return [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "SBIN",
        "LT",
        "ITC",
        "HINDUNILVR",
        "BAJFINANCE"
    ]


if __name__ == "__main__":
    print("Sample NSE Stocks:", get_nse_stocks())
    print("RELIANCE Price:", fetch_nse_quote("RELIANCE"))
