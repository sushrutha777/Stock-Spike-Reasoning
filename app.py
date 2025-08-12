import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Spike Reason Finder", layout="wide")
st.title("📈 AI-Based Stock Spike Reason Finder")

# --- Predefined 20 stocks + Highway Infrastructure ---
stock_options = {
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
    # Newly added IPO with spike
    "Highway Infrastructure": "HILINFRA.NS"
}

selected_name = st.selectbox("🔍 Choose a stock", list(stock_options.keys()))
selected_ticker = stock_options[selected_name]

# --- Load data when user clicks ---
if st.button("🚀 Analyze Spike"):
    st.info(f"Fetching 5-minute data for {selected_name}...")

    try:
        df = yf.download(selected_ticker, interval="5m", period="1d")
        df['pct_change'] = df['Close'].pct_change() * 100
        df.dropna(inplace=True)

        # Detect spikes > ±3%
        spikes = df[abs(df['pct_change']) > 3]

        st.subheader(f"📉 Intraday Price Chart - {selected_name}")
        st.line_chart(df['Close'])

        if not spikes.empty:
            st.subheader("🚨 Spike Detected!")
            for index, row in spikes.tail(3).iterrows():
                st.write(f"🕒 {index.time()} - Change: {row['pct_change']:.2f}%")

            st.success("🔍 Summary: (AI output goes here)")
        else:
            st.success("✅ No spike above ±3% detected today.")
    
    except Exception as e:
        st.error(f"Error fetching data: {e}")
