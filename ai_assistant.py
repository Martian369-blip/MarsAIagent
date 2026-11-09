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

# --- MASTER LAYOUT INITIALIZATION CORE ---
st.set_page_config(page_title="MARS AI Master Agent", page_icon="🛸", layout="wide")

JOURNAL_FILE = "trading_journal.csv"

# ==================== INSTITUTIONAL GRAPHIC INJECTIONS ====================
st.markdown("""
    <style>
    .report-title-card {
        background: linear-gradient(135deg, #1e2638 0%, #0d111a 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2d3748;
        margin-bottom: 20px;
    }
    .ai-research-block {
        background-color: #0f121d;
        padding: 22px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        color: #e2e8f0;
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.7;
        margin-bottom: 15px;
    }
    .tech-metric-tag {
        background-color: #1a202c;
        padding: 4px 10px;
        border-radius: 4px;
        border: 1px solid #4a5568;
        color: #ff9900;
        font-family: monospace;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛸 MARS_AGENT V16.0: MASTER OMNI-RESEARCH DESK")
st.caption("Advanced Conversational NLP Analytics Engine & Visual Media Network Core")

# Lateral parameters base
st.sidebar.markdown("### 🛡️ Capital Security Desk")
wallet_base = st.sidebar.number_input("Wallet Allocation Balance (ZAR)", value=1000.00)
risk_slider = st.sidebar.slider("Maximum Allowed Risk Threshold (%)", 1.0, 10.0, 5.0)

# ==================== DATA ARCHITECTURE COMPILATION LAYER ====================
def parse_market_metrics(ticker):
    try:
        feed = yf.Ticker(ticker)
        df = feed.history(period="1mo", interval="1h")
        if df.empty: return None, None
        
        close_series = pd.Series(df['Close'].values.flatten())
        rsi_vals = ta.momentum.RSIIndicator(close=close_series).rsi().fillna(50.0).values
        ema_vals = ta.trend.EMAIndicator(close=close_series, window=200).ema_indicator().fillna(close_series).values
        atr_vals = ta.volatility.AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close']).average_true_range().fillna(close_series * 0.002).values
        
        # MACD metrics indicators
        macd_obj = ta.trend.MACD(close=close_series)
        macd_line = macd_obj.macd().fillna(0.0).values
        macd_signal = macd_obj.macd_signal().fillna(0.0).values
        
        return {
            "price": float(df['Close'].iloc[-1]),
            "rsi": float(rsi_vals[-1]),
            "ema200": float(ema_vals[-1]),
            "atr": float(atr_vals[-1]),
            "macd_l": float(macd_line[-1]),
            "macd_s": float(macd_signal[-1]),
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
            for item in root.findall('.//item')[:5]:
                title = item.find('title')
                if title is not None and title.text:
                    headlines.append(title.text)
    except Exception:
        pass
    return headlines

def generate_hardened_local_synthesis(ticker, metrics, wallet, max_risk_pct):
    price, ema, rsi, atr = metrics["price"], metrics["ema200"], metrics["rsi"], metrics["atr"]
    regime = "🟢 UPTREND ACCUMULATION" if price > ema else "🔴 DOWNTREND DISTRIBUTION"
    
    mult = 10000 if "USD" in ticker and "=" in ticker else 1
    sl_distance_pts = (atr * 2.0) * mult
    
    if "ZAR" in ticker:
        raw_zar_risk = (atr * 2.0) * 10000 * 0.10
    elif "=" in ticker:
        raw_zar_risk = (atr * 2.0) * 10000 * 0.01 * 18.35
    elif ticker == "GC=F":
        raw_zar_risk = (atr * 2.0) * 1.00 * 18.35 * 100
    else:
        raw_zar_risk = (atr * 2.0) * 1.00 * 18.35
        
    actual_risk_pct = (raw_zar_risk / wallet) * 100
    risk_status = "✅ RISK METRICS APPROVED" if actual_risk_pct <= max_risk_pct else "❌ REJECTED (EXCEEDS PERMITTED SAFE ASSIGNMENT)"
    
    suggested_sl = price - (atr * 2.0) if price > ema else price + (atr * 2.0)
    suggested_tp = price + (atr * 4.0) if price > ema else price - (atr * 4.0)
    
    report = (
        f"📋 **HARDENED LOCAL SYNTHESIS RISK BRIEFING FOR {ticker}**\n\n"
        f"• **Regime Structural State:** The asset is currently executing a trend phase inside an **{regime}** relative to its hourly 200 Exponential Moving Average baseline marker.\n"
        f"• **Momentum Oscillator Parameters:** RSI index coordinates are sitting at **{rsi:.1f}**, confirming active momentum boundaries.\n"
        f"• **Execution Sizing Blueprint (0.01 Contracts):** Suggested Stop Loss is mapped to `{suggested_sl:.4f}` (~{sl_distance_pts:.1f} pts away) with a target Take Profit corridor projected near `{suggested_tp:.4f}`.\n"
        f"• **Capital Defense Ledger Evaluation:** Opening this trade costs an estimated **R{raw_zar_risk:.2f}** in potential risk exposure boundary. Against your wallet budget, this totals **{actual_risk_pct:.1f}%** exposure status. `Sizing Decision: {risk_status}`."
    )
    return report

def run_ai_inference(prompt_text):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.Blackbox,
            messages=[{"role": "user", "content": prompt_text}],
            timeout=10
        )
        return response
    except Exception:
        return "FALLBACK_TRIGGERED"

# ==================== MASTER ANALYSIS WORKSPACE ENTRY ====================
user_query = st.text_input("💬 Query Your Research Agent (e.g., 'Perform comprehensive macro research on Gold Ounce Futures'):", value="")

if user_query:
    # --- INTERLOCK 24/7 DYNAMIC VOCABULARY ASSET MAPPER ---
    target_ticker = "BTC-USD" 
    clean_query = user_query.upper().replace("?", "").replace("'", "")
    
    vocabulary_asset_matrix = {
        "GOLD": "GC=F", "SILVER": "SI=F", "RAND": "USDZAR=X", "ZAR": "USDZAR=X",
        "YEN": "USDJPY=X", "POUND": "GBPUSD=X", "EURO": "EURUSD=X", "NASDAQ": "^NDX",
        "TECH": "^NDX", "CRUDE": "CL=F", "OIL": "BZ=F", "BITCOIN": "BTC-USD", "CRYPTO": "BTC-USD"
    }
    for keyword, ticker_symbol in vocabulary_asset_matrix.items():
        if keyword in clean_query:
            target_ticker = ticker_symbol
            break
    words = clean_query.split()
    for word in words:
        if "=" in word or "-" in word or ".JO" in word or "^" in word:
            target_ticker = word
            break

    st.markdown(f"<div class='report-title-card'>📊 <b>INTELLIGENCE INTERFACE FOCUS NODE:</b> {target_ticker}</div>", unsafe_allow_html=True)
    
    metrics, history_df = parse_market_metrics(target_ticker)
    global_news = extract_news_headlines()
    
    if metrics:
        news_summary = " | ".join(global_news) if global_news else "Consolidated trend volume flow stable."
        
        # Expanded multi-indicator systemic system prompt structure configuration
        ai_context_prompt = (
            f"You are the ultimate advanced institutional quantitative investment AI research assistant. "
            f"Provide an incredibly thorough, professional, and dense technical report analyzing: {target_ticker}.\n"
            f"Live Statistics Baseline Data:\n"
            f"- Price: {metrics['price']}\n"
            f"- RSI Oscillator Value: {metrics['rsi']:.2f}\n"
            f"- 200 EMA Moving Average: {metrics['ema200']:.2f}\n"
            f"- ATR Volatility: {metrics['atr']:.4f}\n"
            f"- MACD Line: {metrics['macd_l']:.4f} | Signal Line: {metrics['macd_s']:.4f}\n"
            f"- News Wire Backdrop Context: {news_summary}\n\n"
            f"Format your response as a rich, multi-paragraph document with explicit markdown subheaders. "
            f"Section 1: Thorough Technical Analysis breakdown explaining MACD crossover status and price orientation relative to 200 hourly EMA. "
            f"Section 2: Deep Market Sentiment Hypothesis drawing conclusions from recent headlines. "
            f"Section 3: Rigorous Sizing & Protective Risk Parameters. Calculate a safe 2x ATR stop level and contrast the resulting Rand cash loss value against a capital wallet baseline of R{wallet_base} under a max risk cap configuration of {risk_slider}%."
        )
        
        with st.spinner("🛸 Activating cognitive analytical modules... Processing real-time data arrays..."):
            ai_response_text = run_ai_inference(ai_context_prompt)
            
        if not ai_response_text or "FALLBACK_TRIGGERED" in ai_response_text or "Copilot" in str(ai_response_text) or "Install" in str(ai_response_text):
            final_report_body = generate_hardened_local_synthesis(target_ticker, metrics, wallet_base, risk_slider)
        else:
            final_report_body = str(ai_response_text)
            
        # Display the rich, multi-paragraph research response bubble
        st.markdown(f"<div class='ai-research-block'>{final_report_body}</div>", unsafe_allow_html=True)
        
        # --- TECHNICAL METRICS DASHBOARD STATUS PANEL ROW ---
        st.markdown("### 🎛️ Live Indicator Reference Telemetry Desk")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"**Trend Engine Baseline**<br><span class='tech-metric-tag'>200 EMA: {metrics['ema200']:.4f}</span>", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"**Momentum Oscillator**<br><span class='tech-metric-tag'>RSI Index: {metrics['rsi']:.1f}</span>", unsafe_allow_html=True)
