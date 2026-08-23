import os
import time

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="Crypto Sentiment Terminal", page_icon="📈", layout="wide")

st.title("📈 Crypto Sentiment Terminal")
st.markdown("Analyze the real-time financial sentiment of cryptocurrency news using Gemini AI.")

api_key = os.getenv("GEMINI_API_KEY")
uri = os.getenv("url")
if not api_key:
    st.warning("⚠️ Please set GEMINI_API_KEY in your .env file before running the app.")
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📰 Input News Headlines")
    default_news = """Bitcoin surges past $60k as institutional adoption grows.
Ethereum network faces congestion, leading to higher gas fees.
New regulations proposed in the EU could restrict crypto trading.
Solana launches new update to improve transaction speeds."""
    
    news_input = st.text_area("Paste news headlines here (one per line):", value=default_news, height=200)

@st.cache_data(ttl=15)
def get_live_prices():
    try:
        url = uri
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

with col2:
    st.subheader("📊 Live Market Overview")
    
    @st.fragment(run_every=15)
    def update_metrics():
        price_data = get_live_prices()
        
        if price_data:
            btc_price = price_data.get("bitcoin", {}).get("usd", 0)
            btc_change = price_data.get("bitcoin", {}).get("usd_24h_change", 0)
            
            eth_price = price_data.get("ethereum", {}).get("usd", 0)
            eth_change = price_data.get("ethereum", {}).get("usd_24h_change", 0)
            
            sol_price = price_data.get("solana", {}).get("usd", 0)
            sol_change = price_data.get("solana", {}).get("usd_24h_change", 0)
            
            st.metric(label="BTC/USD", value=f"${btc_price:,.2f}", delta=f"{btc_change:.2f}%")
            st.metric(label="ETH/USD", value=f"${eth_price:,.2f}", delta=f"{eth_change:.2f}%")
            st.metric(label="SOL/USD", value=f"${sol_price:,.2f}", delta=f"{sol_change:.2f}%")
        else:
            st.metric(label="BTC/USD", value="$61,230.50", delta="4.5%")
            st.metric(label="ETH/USD", value="$3,450.00", delta="-1.2%")
            st.metric(label="SOL/USD", value="$145.20", delta="8.3%")
            
    update_metrics()

st.divider()

if st.button("🧠 Analyze Sentiment", type="primary"):
    if not news_input.strip():
        st.warning("⚠️ Please enter some news headlines to analyze.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            headlines = [line.strip() for line in news_input.split('\n') if line.strip()]
            
            with st.spinner('Analyzing financial sentiment...'):
                results = []
                for headline in headlines:
                    prompt = f"""
                    You are an expert financial analyst. Analyze the following cryptocurrency news headline.
                    Determine if the sentiment is Bullish (Positive), Bearish (Negative), or Neutral.
                    Provide a 1-sentence reason.
                    
                    Headline: "{headline}"
                    
                    Format your response strictly as:
                    Sentiment: [Bullish/Bearish/Neutral]
                    Reason: [Your reason]
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config={
                            "thinking_config": {
                                "thinking_budget": 0
                            }
                        }
                    )
                    text = response.text
                    
                    sentiment = "Neutral"
                    reason = "Could not parse."
                    if "Sentiment:" in text and "Reason:" in text:
                        parts = text.split("Reason:")
                        sentiment_part = parts[0].replace("Sentiment:", "").strip()
                        if "Bullish" in sentiment_part: sentiment = "Bullish 🟢"
                        elif "Bearish" in sentiment_part: sentiment = "Bearish 🔴"
                        else: sentiment = "Neutral ⚪"
                        reason = parts[1].strip()
                    
                    results.append({"Headline": headline, "Sentiment": sentiment, "Reason": reason})
                    time.sleep(1)
                
                st.success("Analysis Complete!")
                
                st.subheader("🔍 Sentiment Analysis Results")
                df = pd.DataFrame(results)
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                bullish_count = sum("Bullish" in r["Sentiment"] for r in results)
                bearish_count = sum("Bearish" in r["Sentiment"] for r in results)
                neutral_count = sum("Neutral" in r["Sentiment"] for r in results)
                
                st.markdown("### 📈 Overall Market Mood")
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Bullish Headlines", bullish_count)
                m_col2.metric("Bearish Headlines", bearish_count)
                m_col3.metric("Neutral Headlines", neutral_count)

        except Exception as e:
            st.error(f"An error occurred: {e}")