import streamlit as st
from openai import OpenAI
import pandas as pd
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Trading Desk - AI Multi-Agent Hub",
    page_icon="📈",
    layout="wide"
)

# --- Styling & Layout ---
st.title("Trading Desk 🔥")
st.markdown("### 6 AI Agents Collaborating 24/7 on Live Market Strategy")

# Sidebar for API Keys and Settings
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.markdown("---")
    st.markdown("### Active Bots")
    st.markdown("👑 **Chief** (Strategy Coordinator)")
    st.markdown("🔭 **Scout** (Market Screener)")
    st.markdown("📰 **News** (Macro & Headlines)")
    st.markdown("📊 **Sentiment** (Social & Fear/Greed)")
    st.markdown("📉 **Charts** (Technical Indicators)")
    st.markdown("🛡️ **Skeptic** (Risk Manager)")

# Check API Key
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to start interacting with the agents.")

# --- Simulated Portfolio / Desk PnL Header ---
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("DESK P&L (TODAY)", "+$2,569", "+14.2%")
col2.metric("BTC / USD", "$91,420", "+3.8%")
col3.metric("ETH / USD", "$3,340", "+2.1%")
col4.metric("SOL / USD", "$215", "+4.4%")
st.markdown("---")

# --- Main Interaction Hub ---
st.subheader("💬 Group Chat: Live Trading Floor")

user_prompt = st.text_input("Ask the trading desk a question or give a command (e.g., 'Should we long SOL right now?'):", "Analyze BTC and recommend a trade setup for today.")

if st.button("Run Multi-Agent Analysis"):
    if not api_key:
        st.error("Please provide an OpenAI API key first.")
    else:
        client = OpenAI(api_key=api_key)
        
        with st.spinner("🤖 The 6 AI Bots are debating strategy..."):
            scout_box = st.empty()
            news_box = st.empty()
            sentiment_box = st.empty()
            charts_box = st.empty()
            skeptic_box = st.empty()
            chief_box = st.empty()
            
            agents = {
                "Scout": "You are Scout, a crypto market scanner bot. Focus on volume spikes, live price momentum, and immediate liquidity shifts.",
                "News": "You are News, a macro and crypto news parser bot. Focus on recent headlines, regulatory updates, and upcoming catalysts.",
                "Sentiment": "You are Sentiment, a social mood analyst bot. Track fear/greed, X (Twitter) chatter, and community hype.",
                "Charts": "You are Charts, a technical analysis bot. Focus on RSI, moving averages, support/resistance levels, and chart patterns.",
                "Skeptic": "You are Skeptic, a brutal risk manager bot. Look for flaws, market traps, over-leveraging signs, and reasons NOT to take the trade.",
                "Chief": "You are Chief, the head coordinator bot. Review inputs from Scout, News, Sentiment, Charts, and Skeptic, then make the final call (Long, Short, or Stay Out)."
            }
            
            def call_agent(role_prompt, context):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": role_prompt},
                            {"role": "user", "content": f"User query: {user_prompt}\n\nContext/Previous thoughts: {context}"}
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    return f"Error communicating with agent: {e}"

            time.sleep(0.5)
            scout_res = call_agent(agents["Scout"], "")
            scout_box.markdown(f"🔭 **Scout:** {scout_res}")
            
            time.sleep(0.5)
            news_res = call_agent(agents["News"], scout_res)
            news_box.markdown(f"📰 **News:** {news_res}")
            
            time.sleep(0.5)
            sentiment_res = call_agent(agents["Sentiment"], news_res)
            sentiment_box.markdown(f"📊 **Sentiment:** {sentiment_res}")
            
            time.sleep(0.5)
            charts_res = call_agent(agents["Charts"], sentiment_res)
            charts_box.markdown(f"📉 **Charts:** {charts_res}")
            
            time.sleep(0.5)
            skeptic_res = call_agent(agents["Skeptic"], charts_res)
            skeptic_box.markdown(f"🛡️ **Skeptic:** {skeptic_res}")
            
            combined_context = f"Scout: {scout_res}\nNews: {news_res}\nSentiment: {sentiment_res}\nCharts: {charts_res}\nSkeptic: {skeptic_res}"
            time.sleep(0.8)
            chief_res = call_agent(agents["Chief"], combined_context)
            chief_box.markdown(f"👑 **Chief (Final Verdict):** {chief_res}")
            
        st.success("Analysis complete!")
                  
