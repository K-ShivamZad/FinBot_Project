import streamlit as st
import plotly.express as px
import pandas as pd
import time
import sqlite3 
from db_handler import add_transaction, get_transactions, DB_NAME
from brain import process_text

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="FinBot AI Core", page_icon="⚡", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stChatInputContainer { border-color: #00D4FF !important; }
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: scale(1.02); border-color: #00D4FF;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif; font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00D4FF, #9B4DCA);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Budget & Controls) ---
with st.sidebar:
    st.header("⚙️ CONTROL PANEL")
    
    # 1. SET BUDGET GOAL
    budget = st.slider("Monthly Budget Goal (₹)", 1000, 50000, 10000, step=500)
    
    # 2. RESET BUTTON 
    st.markdown("---")
    if st.button("⚠️ FACTORY RESET DATA"):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM transactions")
        conn.commit()
        conn.close()
        st.rerun()

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1: st.markdown("# ⚡") 
with col2:
    st.title("FINBOT CORE")
    st.caption("AUTONOMOUS NLP FINANCIAL TRACKING SYSTEM // LOCAL COMPILATION")

st.markdown("---")

# --- MAIN DASHBOARD ---
placeholder = st.empty()

def update_dashboard():
    df = get_transactions()
    with placeholder.container():
        if not df.empty:
            total_spent = df['amount'].sum()
            
            # --- SMART BUDGET ALERT ---
            budget_percent = (total_spent / budget) * 100
            
            st.markdown(f"### 🎯 BUDGET UTILIZATION: {round(budget_percent)}%")
            st.progress(min(budget_percent / 100, 1.0))
            
            if budget_percent > 100:
                st.error(f"🚨 CRITICAL ALERT: Budget Exceeded by ₹{total_spent - budget}!")
            
            st.markdown("---")

            # METRICS
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("💰 TOTAL SPEND", f"₹{total_spent:,.0f}")
            m2.metric("💳 TRANSACTIONS", len(df))
            m3.metric("🛒 LAST PURCHASE", df.iloc[-1]['item'])
            m4.metric("📉 REMAINING", f"₹{max(budget - total_spent, 0):,.0f}")

            # CHARTS
            c1, c2 = st.columns([2, 1])
            with c1:
                daily_trend = df.groupby('date')['amount'].sum().reset_index()
                fig_line = px.line(daily_trend, x='date', y='amount', title="Spending Timeline", markers=True)
                fig_line.update_traces(line_color='#00D4FF', line_width=4)
                fig_line.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_line, width=1000) 
            
            with c2:
                fig_pie = px.pie(df, values='amount', names='category', hole=0.6, title="Category Distribution", color_discrete_sequence=px.colors.sequential.Blues)
                fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)

            with st.expander("🔍 VIEW RAW LOGS"):
                st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)
        
        else:
            st.info("SYSTEM READY. AWAITING INPUT.")

update_dashboard()

# --- CHAT INPUT (NLP) ---
if prompt := st.chat_input("Enter command... (e.g., 'Spent 4500 on Flight Tickets')"):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        with st.status("⚙️ NLP Engine Processing...", expanded=True) as status:
            time.sleep(0.5)
            st.write("Applying Regex Rules...")
            data = process_text(prompt)
            
            if data["valid"]:
                add_transaction(data["item"], data["category"], data["amount"])
                status.update(label="Transaction Logged", state="complete", expanded=False)
                update_dashboard()
                st.success(f"Confirmed: ₹{data['amount']} debited for {data['item']}")
            else:
                status.update(label="Parsing Failed", state="error")
                st.error("❌ Command not recognized. Ensure you include a number (e.g., '500 for food').")