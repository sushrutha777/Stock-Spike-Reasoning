import streamlit as st
import os
from dotenv import load_dotenv
import plotly.graph_objects as go

from backend.spike_detector import get_recent_data, detect_spike
from backend.news_fetcher import fetch_news_rss
from backend.reasoning import generate_reasoning
from utils.stock_list import DEFAULT_STOCKS

# Load env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Stock Spike Reasoning", layout="wide")

st.title("📈 Stock Spike Reasoning (AI Powered)")
st.write("Detects stock price spikes and explains them using news + Gemini reasoning.")

# --- Stock Selector ---
ticker = st.selectbox("Choose Stock:", DEFAULT_STOCKS, index=0)

# --- Spike threshold ---
threshold = st.slider("Spike Detection Threshold (%)", 0.0, 10.0, 3.0, step=0.5)

# --- Day range ---
days_range = st.slider("Select Day Range for Analysis", 1, 30, 7)

if st.button("🔍 Analyze"):
    with st.spinner("Fetching stock data..."):
        period = f"{days_range}d"
        df = get_recent_data(ticker, period=period)

    if df is None or df.empty:
        st.error("No data found. Check ticker symbol.")
    else:
        # Interactive Plotly chart
        st.subheader(f"📊 Closing Prices (Last {days_range} Days)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines+markers", name="Close Price"))
        fig.update_layout(title=f"{ticker} Stock Closing Prices",
                          xaxis_title="Date",
                          yaxis_title="Price (USD)",
                          template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # Spike detection
        is_spike, last_change = detect_spike(df, threshold)
        last_change_str = f"{last_change:.2f}%" if last_change is not None else "N/A"

        if is_spike:
            st.success(f"✅ Spike detected: {ticker} moved {last_change_str} (Threshold: {threshold}%)")

            st.write("Recent % changes:")
            st.dataframe(df[["Close", "PctChange"]].tail(days_range).round(2))

            # Fetch news
            st.subheader("📰 Latest News Headlines")
            with st.spinner("Fetching news..."):
                headlines = fetch_news_rss(ticker, max_headlines=5)

            if headlines:
                for h in headlines:
                    st.markdown(f"- [{h['title']}]({h['link']})", unsafe_allow_html=True)
            else:
                st.write("No headlines found.")

            # AI Reasoning
            stock_info = f"{ticker} moved {last_change_str} in last {days_range} days."
            st.subheader("🤖 AI Summary (Gemini)")
            with st.spinner("Generating explanation..."):
                reasoning_text = generate_reasoning(stock_info, headlines, api_key=GEMINI_API_KEY)
            st.write(reasoning_text)

            if st.button("🔄 Regenerate Explanation"):
                with st.spinner("Regenerating..."):
                    reasoning_text = generate_reasoning(stock_info, headlines, api_key=GEMINI_API_KEY)
                st.write(reasoning_text)

        else:
            st.info(f"ℹ️ No spike detected for {ticker} in last {days_range} days. Last change: {last_change_str} (Threshold: {threshold}%)")

st.markdown("---")
st.caption("Built with Streamlit, yfinance, Plotly, Google News RSS, and Gemini API • Team: Sushrutha & Group")
