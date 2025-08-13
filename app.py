import streamlit as st
from backend.spike_detector import get_recent_prices, detect_spike
from backend.news_fetcher import fetch_google_news
from backend.tweet_fetcher import fetch_tweets
from backend.summarizer import summarize_reason
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Spike Reason Finder", layout="wide")
st.title("📈 Stock Spike Reason Finder (100% Free)")

stocks = [
    "NVDA",        # Recent spike after earnings
    "TSLA",        # Frequent big swings
    "AAPL", 
    "MSFT", 
    "GOOGL", 
    "AMZN", 
    "INFY.NS", 
    "RELIANCE.NS", # Recent jump in India
    "TCS.NS"
]

col1, col2 = st.columns([2, 1])
with col1:
    stock = st.selectbox("Select a stock", stocks)
with col2:
    test_mode = st.checkbox("Test Mode (1% spike threshold)", value=False)

if st.button("Analyze Spike"):
    df = get_recent_prices(stock)
    if df is None or len(df) < 2:
        st.error("Not enough data to analyze.")
    else:
        # Interactive stock chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines+markers', name='Close Price'))
        fig.update_layout(title=f"{stock} Price Chart", xaxis_title="Date", yaxis_title="Price", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # Detect spike
        threshold = 1 if test_mode else 5
        spike, pct_change = detect_spike(df, threshold)
        if not spike:
            st.info(f"No significant spike detected (Δ{pct_change:.2f}%)")
        else:
            st.success(f"Spike detected! Change: {pct_change:.2f}%")
            
            # Fetch news & tweets
            news = fetch_google_news(stock)
            tweets = fetch_tweets(f"{stock} stock")
            
            st.subheader("📰 Recent News Headlines")
            if news:
                for n in news:
                    st.write(f"- {n}")
            else:
                st.write("No recent news found.")
            
            st.subheader("🐦 Recent Tweets")
            if tweets:
                for t in tweets:
                    st.write(f"- {t}")
            else:
                st.write("No recent tweets found.")
            
            # Summarize reason
            st.subheader("🤖 AI-Generated Spike Reason")
            summary = summarize_reason(stock, news, tweets)
            st.write(summary)
