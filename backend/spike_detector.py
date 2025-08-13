import yfinance as yf

def get_recent_prices(ticker):
    try:
        df = yf.Ticker(ticker).history(period="7d")
        return df
    except:
        return None

def detect_spike(df, threshold=5):
    if len(df) < 2:
        return False, 0
    latest_close = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2]
    pct_change = ((latest_close - prev_close) / prev_close) * 100
    return abs(pct_change) >= threshold, pct_change
