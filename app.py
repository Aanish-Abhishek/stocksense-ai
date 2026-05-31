import streamlit as st
from api import analyse_stock, StockRequest  # import your API function and request model
from agent import agent  # import your agent from your agent file

# ── Page Config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StockSense AI",
    page_icon="📈",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────────────────────
st.title("📈 StockSense AI")
st.markdown("*Real-time Stock Research Assistant powered by AI Agent*")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Stock Lookup")
    st.markdown("*Indian Stocks (NSE)*")
    st.caption("RELIANCE.NS · TCS.NS · INFY.NS · HDFC.NS")
    st.markdown("*US Stocks*")
    st.caption("AAPL · TSLA · MSFT · GOOGL")
    st.divider()
    st.markdown("*How it works:*")
    st.markdown("1. Enter a stock ticker")
    st.markdown("2. AI agent fetches live price")
    st.markdown("3. Agent fetches latest news")
    st.markdown("4. GPT-4o mini analyses everything")
    st.markdown("5. Get Buy/Hold/Sell signal")

# ── Input ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    ticker = st.text_input(
        "Enter stock ticker",
        placeholder="e.g. RELIANCE.NS or AAPL",
        label_visibility="collapsed"
    )

with col2:
    analyse_btn = st.button("🔍 Analyse", use_container_width=True)

# ── Analysis ──────────────────────────────────────────────────────────────
if analyse_btn:
    if not ticker:
        st.warning("⚠️ Please enter a stock ticker first.")
        st.stop()

    with st.spinner(f"Analysing {ticker.upper()} — fetching price, news and generating insights..."):
        try:
            output = analyse_stock(StockRequest(ticker=ticker))

            # ── Signal Badge ──────────────────────────────────────────────
            signal_color = "🟢" if "Buy" in output else "🔴" if "Sell" in output else "🟡"
            sentiment_color = "🟢" if "Bullish" in output else "🔴" if "Bearish" in output else "🟡"

            # ── Metrics Row ───────────────────────────────────────────────
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Stock", ticker.upper())
            with m2:
                if "Bullish" in output:
                    st.metric("Sentiment", "Bullish 🟢")
                elif "Bearish" in output:
                    st.metric("Sentiment", "Bearish 🔴")
                else:
                    st.metric("Sentiment", "Neutral 🟡")
            with m3:
                if "Buy" in output:
                    st.metric("Signal", "Buy 🟢")
                elif "Sell" in output:
                    st.metric("Signal", "Sell 🔴")
                else:
                    st.metric("Signal", "Hold 🟡")

            st.divider()

            # ── Full Analysis ─────────────────────────────────────────────
            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error analysing {ticker}: {str(e)}")
            st.caption("Make sure the ticker format is correct. Use .NS suffix for Indian stocks.")