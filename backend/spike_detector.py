import yfinance as yf
import pandas as pd

def detect_spikes(ticker: str, interval="15m", threshold=1):
    # Download intraday data (free from Yahoo Finance)
    data = yf.download(ticker, period="1d", interval=interval)
    data['pct_change'] = data['Close'].pct_change() * 100

    spikes = []
    for i in range(1, len(data)):
        change = data['pct_change'].iloc[i]
        if abs(change) >= threshold:
            spikes.append({
                "time": data.index[i].strftime("%I:%M %p"),
                "change": round(change, 2)
            })

    return spikes, data
