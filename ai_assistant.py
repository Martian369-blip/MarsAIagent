import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import urllib.request
import xml.etree.ElementTree as ET
import plotly.graph_objects as go
from datetime import datetime
import g4f

# --- STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="MARS AI Assistant", page_icon="🧠", layout="wide")

# ==================== ADVANCED VISUAL GRAPHIC STYLING ====================
st.markdown("""
    <style>
    .ai-bubble {
        background-color: #1e222b;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin-bottom: 12px;
        color: white;
        font-family: sans-serif;
        line-height: 1.6;
    }
    .metric-tag {
        color: #ff9900;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 MARS CORE: AI NATURAL INTELLIGENCE CO-PILOT")
st.caption("Conversational Trade Sizing & Sentiment Network Core")

# Lateral parameters base
st.sidebar.markdown("### 🛡️ Capital Profile")
wallet_base = st.sidebar.number_input("Wallet Balance (ZAR)", value=1000.00)
risk_slider = st.sidebar.slider("Max Allowed Allocation Risk (%)", 1.0, 10.0, 5.0)

# ==================== ANALYTICAL DATA ENGINE INJECTORS ====================
def parse_market_metrics(ticker):
    try:
        feed = yf.Ticker(ticker)
        df = feed.history(period="1mo", interval="1h")
        if df.empty: return None, None
        
        close_series = pd.Series(df['Close'].values.flatten())
        rsi_vals = ta.momentum.RSIIndicator(close=close_series).rsi().fillna(50.0).values
        ema_vals = ta.trend.EMAIndicator(close=close_series, window=200).ema_indicator().fillna(close_series).values
        atr_vals = ta.volatility.AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close']).average_true_range().fillna(close_series * 0.002).values
        
        return {
            "price": float(df['Close'].iloc[-1]),
            "rsi": float(rsi_vals[-1]),
            "ema200": float(ema_vals[-1]),
            "atr": float(atr_vals[-1]),
            "ticker_obj": feed
        }, df
    except Exception:
        return None, None

def extract_news_headlines():
    headlines = []
    rss_url = "https://cnbc.com"
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            root = ET.fromstring(response.read())
            for item in root.findall('.//item')[:4]:
                title = item.find('title')
                if title is not None and title.text:
                    headlines.append(title.text)
    except Exception:
        pass
    return headlines

def generate_hardened_local_synthesis(ticker, metrics, wallet, max_risk_pct):
    """
    Algorithmic Interception Layer: Synthesizes a structured financial 
    co-pilot report locally from data elements when cloud servers loop noise.
    """
    price = metrics["price"]
    ema = metrics["ema200"]
    rsi = metrics["rsi"]
    atr = metrics["atr"]
    
    # 1. Trend Regime Definition
    regime = "🟢 UPTREND (BULLISH ACCUMULATION)" if price > ema else "🔴 DOWNTREND (BEARISH DISTRIBUTION)"
    proximity = abs(price - ema) / ema * 100
    
    # 2. Risk Sizing Logic Engine
    mult = 10000 if "USD" in ticker and "=" in ticker else 1
    sl_distance_pts = (atr * 2.0) * mult
    
    # Estimate raw ZAR cost bounds for a standard 0.01 lot contract
    if "ZAR" in ticker:
        raw_zar_risk = (atr * 2.0) * 10000 * 0.10
    elif "=" in ticker:  # Global FX
        raw_zar_risk = (atr * 2.0) * 10000 * 0.01 * 18.35
    else:  # Commodities / Equities
        raw_zar_risk = (atr * 2.0) * 1.00 * 18.35
        
    actual_risk_pct = (raw_zar_risk / wallet) * 100
    risk_status = "✅ APPROVED" if actual_risk_pct <= max_risk_pct else "❌ REJECTED (EXCEEDS SAFETY CAP)"
    
    # 3. Dynamic Stop Formatter
    suggested_sl = price - (atr * 2.0) if price > ema else price + (atr * 2.0)
    suggested_tp = price + (atr * 4.0) if price > ema else price - (atr * 4.0)
    
    report = (
        f"### 🛰️ MARS Strategic Analysis Matrix: {ticker}\n\n"
        f"1. **Market Regime Profile:** Currently trading inside a **{regime}** relative to the 200 Hourly EMA framework. "
        f"The current price is trading at <span class='metric-tag'>{price:.4f}</span> with an RSI momentum coordinates score of **{rsi:.1f}**, signaling short-term trend extensions.\n\n"
        f"2. **Risk Parameters & Protection Vectors (0.01 Micro Sizing):**\n"
        f"   - 🛑 **Suggested Stop Loss (SL):** `{suggested_sl:.4f}` (~{sl_distance_pts:.1f} points away)\n"
        f"   - 🏁 **Suggested Take Profit (TP):** `{suggested_tp:.4f}` (Calibrated for a clean 1:2 Risk-to-Reward profile)\n\n"
        f"3. **Capital Guard Evaluation Ticket:** Real cash portfolio exposure is calculated at **R{raw_zar_risk:.2f}** per 0.01 lot configuration. "
        f"Against your R{wallet:.2f} baseline, this represents an account exposure profile of **{actual_risk_pct:.1f}%**. "
        f"**Sizing Status:** `{risk_status}`. Adjust your entry orders manually inside your mobile terminal to match these boundary layers."
    )
    return report

def run_ai_inference(prompt_text):
    try:
        # Forcing a reliable, alternate free provider channel to clear noise
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.Blackbox,
            messages=[{"role": "user", "content": prompt_text}],
            timeout=10
        )
        return response
    except Exception:
        return "FALLBACK_TRIGGERED"

# ==================== MASTER ASSISTANT WORKSPACE ====================
user_query = st.text_input("💬 Ask your AI Trading Co-Pilot (e.g., 'Analyze EURUSD=X' or 'Is GBPUSD=X a buy?'):", value="")

if user_query:
    st.markdown("### 🧠 AI Analysis Pipeline Output")
    
    # Isolate ticker token from query string string arrays
    target_ticker = "EURUSD=X"
    words = user_query.upper().replace("?", "").replace("'", "").split()
    for word in words:
        if "=" in word or "-" in word or ".JO" in word:
            target_ticker = word
            break
            
    metrics, history_df = parse_market_metrics(target_ticker)
    global_news = extract_news_headlines()
    
    if metrics:
        news_summary = " | ".join(global_news) if global_news else "Consolidated trend volume flow stable."
        
        ai_context_prompt = (
            f"Provide a brief, tactical trading assessment in 3 bullet points maximum for {target_ticker}. "
            f"Spot Price: {metrics['price']}. RSI: {metrics['rsi']:.2f}. 200 EMA: {metrics['ema200']:.2f}. "
            f"Enforce strict capital defense warnings tailored for a small R{wallet_base} account budget profile."
        )
        
        with st.spinner("🧠 Synthesizing real-time analytics matrix..."):
            ai_response_text = run_ai_inference(ai_context_prompt)
            
        # Hardened Interception check to instantly override provider garbage strings
        if not ai_response_text or "FALLBACK_TRIGGERED" in ai_response_text or "Copilot" in str(ai_response_text) or "Install" in str(ai_response_text):
            final_output_report = generate_hardened_local_synthesis(target_ticker, metrics, wallet_base, risk_slider)
        else:
            final_output_report = str(ai_response_text)
            
        st.markdown(f"<div class='ai-bubble'>{final_output_report}</div>", unsafe_allow_html=True)
        
        with st.expander("📊 View Reference Strategy Chart Matrix"):
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=history_df.tail(60).index, open=history_df.tail(60)['Open'], high=history_df.tail(60)['High'], low=history_df.tail(60)['Low'], close=history_df.tail(60)['Close']))
            fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", height=380, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Searching broad global context... Please explicitly type a valid ticker symbol (like EURUSD=X) to pull real-time execution matrices.")
