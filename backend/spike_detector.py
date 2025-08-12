import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def fetch_intraday(symbol: str, period="7d", interval="5m") -> pd.DataFrame:
    """Fetch recent intraday data using yfinance."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval, actions=False)
    if df.empty:
        return df
    df = df.reset_index()
    df.rename(columns={"Datetime": "datetime", "Date": "datetime"}, inplace=True)
    return df


def detect_spikes(df: pd.DataFrame, price_col="Close", window=6, z_thresh=3.0) -> pd.DataFrame:
    """Detect spikes using z-score on percent returns over a rolling window.

    - window: number of intervals for rolling volatility (e.g., 6 for 30 minutes if interval=5m)
    - z_thresh: threshold for z-score to consider as spike
    """
    if df.empty:
        return pd.DataFrame()

    df = df.copy()
    # compute percentage return
    df['pct_change'] = df[price_col].pct_change() * 100

    # rolling mean and std of pct_change
    df['vol_mean'] = df['pct_change'].rolling(window=window, min_periods=1).mean()
    df['vol_std'] = df['pct_change'].rolling(window=window, min_periods=1).std().fillna(0.0)

    # avoid division by zero
    df['z_score'] = (df['pct_change'] - df['vol_mean']) / (df['vol_std'].replace(0, np.nan))
    df['z_score'] = df['z_score'].fillna(0.0)

    # mark spikes
    df['is_spike'] = df['z_score'].abs() > z_thresh

    # summarize spikes
    spikes = df[df['is_spike']].copy()
    spikes['magnitude_pct'] = spikes['pct_change']
    return spikes


if __name__ == "__main__":
    # quick test
    sym = "AAPL"
    df = fetch_intraday(sym, period="3d", interval="5m")
    spikes = detect_spikes(df)
    print(f"Found {len(spikes)} spikes for {sym}")