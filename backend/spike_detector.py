"""
Utilities to fetch price data (yfinance) and detect spikes using rolling z-score on percent returns.
"""
from typing import Optional
import pandas as pd
import numpy as np
import yfinance as yf


def fetch_yf(ticker: str, interval: str = "5m", period: str = "1d") -> pd.DataFrame:
    """Download data via yfinance and flatten MultiIndex columns if present.

    Returns a DataFrame (may be empty).
    """
    df = yf.download(ticker, interval=interval, period=period, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [" ".join(col).strip() for col in df.columns.values]
    return df


def detect_spikes(df: pd.DataFrame, price_col: str = "Close", window: int = 6, z_thresh: float = 3.0, min_pct: float = 0.5) -> pd.DataFrame:
    """Detect spikes using rolling z-score of percent returns.

    - window: rolling window size (e.g., 6 for 30 minutes if interval=5m)
    - z_thresh: absolute z-score threshold
    - min_pct: minimum absolute percent-move to consider (to avoid tiny noise)

    Returns a DataFrame containing only spike rows with additional columns:
    ['pct_change', 'vol_mean', 'vol_std', 'z_score', 'is_spike', 'magnitude_pct']
    """
    if df is None or df.empty or price_col not in df.columns:
        return pd.DataFrame()

    df = df.copy()
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df.dropna(subset=[price_col], inplace=True)

    # percent change in percent units
    df["pct_change"] = df[price_col].pct_change() * 100

    # rolling mean/std
    df["vol_mean"] = df["pct_change"].rolling(window=window, min_periods=1).mean()
    df["vol_std"] = df["pct_change"].rolling(window=window, min_periods=1).std(ddof=0)

    # avoid division by zero
    df["vol_std"] = df["vol_std"].replace(0, np.nan)

    df["z_score"] = (df["pct_change"] - df["vol_mean"]) / df["vol_std"]
    df["z_score"] = df["z_score"].fillna(0.0)

    df["is_spike"] = (df["z_score"].abs() > z_thresh) & (df["pct_change"].abs() >= min_pct)

    spikes = df[df["is_spike"]].copy()
    spikes["magnitude_pct"] = spikes["pct_change"]
    return spikes