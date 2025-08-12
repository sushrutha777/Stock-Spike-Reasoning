# app.py
import streamlit as st
import pandas as pd
from typing import Dict

# backend modules (ensure these files exist under backend/)
from backend.spike_detector import fetch_yf, detect_spikes
from backend.news_fetcher import fetch_google_news_for_symbol
from backend.tweet_fetcher import fetch_tweets_by_query
from backend.summarizer import summarize_text
from backend.nse_fetcher import fetch_nse_quote

st.set_page_config(page_title="Stock Spike Reason Finder", layout="wide")
st.title("📈 AI-Based Stock Spike Reason Finder")

# --- Stocks to monitor (20 notable picks) ---
STOCK_OPTIONS: Dict[str, str] = {
    "Infosys": "INFY.NS",
    "TCS": "TCS.NS",
    "Reliance Industries": "RELIANCE.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Wipro": "WIPRO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "State Bank of India": "SBIN.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Larsen & Toubro": "LT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Coal India": "COALINDIA.NS",
    "ONGC": "ONGC.NS",
    "Power Grid": "POWERGRID.NS",
    "Zomato": "ZOMATO.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "NTPC": "NTPC.NS",
}

# --- UI inputs ---
selected_name = st.selectbox("🔍 Choose a stock", list(STOCK_OPTIONS.keys()), index=0)
selected_ticker = STOCK_OPTIONS[selected_name]

st.markdown(f"**Ticker:** `{selected_ticker}`")

# Parameters in sidebar
with st.sidebar:
    st.header("Analysis Settings")
    z_thresh = st.slider("Spike z-score threshold", 2.0, 6.0, 3.0, step=0.5)
    window = st.slider("Rolling window (intervals)", 3, 20, 6)
    min_pct = st.slider("Min % move to consider a spike", 0.1, 10.0, 0.5, step=0.1)
    fetch_news = st.checkbox("Fetch news (Google News)", value=True)
    fetch_tweets = st.checkbox("Fetch tweets (snscrape)", value=False)
    cache_ttl = st.number_input("Cache TTL (seconds)", value=60, min_value=10)

# caching wrappers to avoid repeated network calls
@st.cache_data(ttl=60)
def get_yf_data(ticker: str, interval: str, period: str):
    """Wrapper around fetch_yf from backend to be cacheable by Streamlit."""
    return fetch_yf(ticker, interval=interval, period=period)

@st.cache_data(ttl=60)
def get_nse_quote(symbol: str):
    return fetch_nse_quote(symbol)

# Analyze button
if st.button("🚀 Analyze Spike"):
    st.info(f"Fetching price data for {selected_name} ({selected_ticker})...")

    # --- Robust data-fetching strategy ---
    # 1) Try intraday 5m for 1 day
    df = get_yf_data(selected_ticker, interval="5m", period="1d")

    # 2) Fall back to last 30 days daily
    if df is None or df.empty or "Close" not in df.columns:
        st.warning("No intraday data found. Trying last 30 days of daily data...")
        df = get_yf_data(selected_ticker, interval="1d", period="30d")

    # 3) Fall back to 6 months daily
    if df is None or df.empty or "Close" not in df.columns:
        st.warning("No daily data in last 30 days. Trying last 6 months...")
        df = get_yf_data(selected_ticker, interval="1d", period="6mo")

    # 4) NSE fallback (use exchange quote to build a 1-row DataFrame)
    if df is None or df.empty or "Close" not in df.columns:
        st.warning("yfinance returned no usable data — attempting NSE fallback...")
        q = get_nse_quote(selected_ticker.replace('.NS',''))
        if q and q.get("df") is not None:
            df = q.get("df")
            st.success("Using NSE quote as a single-row fallback.")
        else:
            st.error("No data available for this stock (yfinance & NSE fallback failed).")
            st.stop()

    # final sanity checks
    if df is None or df.empty:
        st.error("Fetched data is empty after all fallbacks.")
        st.stop()

    if "Close" not in df.columns:
        st.error("Fetched data does not contain 'Close' prices.")
        st.stop()

    # ensure numeric Close
    df = df.copy()
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df.dropna(subset=["Close"], inplace=True)
    if df.empty:
        st.error("No numeric Close prices found after cleaning.")
        st.stop()

    # compute pct change and run spike detector
    df["pct_change"] = df["Close"].pct_change() * 100
    spikes = detect_spikes(df, price_col="Close", window=window, z_thresh=z_thresh, min_pct=min_pct)

    # show chart
    st.subheader(f"📉 Price Chart - {selected_name}")
    st.line_chart(df["Close"])

    # show spikes table or message
    if spikes.empty:
        st.success("✅ No spikes detected in this period.")
    else:
        st.subheader("🚨 Spikes detected")
        st.dataframe(spikes[["pct_change", "z_score", "magnitude_pct"]].tail(10))

        # fetch related news and tweets and summarize
        combined_text_parts = []

        if fetch_news:
            st.info("Fetching news...")
            news_items = fetch_google_news_for_symbol(selected_name, top_n=6)
            if news_items:
                st.write("### Top news")
                for n in news_items:
                    st.write(f"- [{n.get('title')}]({n.get('link')})")
                    combined_text_parts.append((n.get('title', '') + '. ' + n.get('snippet', '')).strip())
            else:
                st.write("No news items found.")

        if fetch_tweets:
            st.info("Fetching tweets (may take a few seconds)...")
            tweets = fetch_tweets_by_query(selected_name, max_tweets=50)
            if tweets:
                st.write("### Sample tweets")
                for t in tweets[:5]:
                    st.write(t.get('content', ''))
                    combined_text_parts.append(t.get('content', ''))
            else:
                st.write("No tweets found (snscrape may not be installed or returned no results).")

        combined_text = " \n ".join([p for p in combined_text_parts if p])
        if combined_text.strip():
            st.subheader("🔍 Suggested reason for spike (summarized)")
            summary = summarize_text(combined_text, max_sentences=3)
            st.write(summary)
        else:
            st.warning("No news or tweets found to summarize for this spike.")

    st.info("Analysis complete. You can tweak parameters in the sidebar and run again.")