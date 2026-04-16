import streamlit as st
import plotly.express as px
import pandas as pd
import time
import sqlite3 
from db_handler import add_transaction, get_transactions, create_user, verify_user, DB_NAME
from brain import process_text

st.set_page_config(page_title="FinBot AI Core", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stChatInputContainer { border-color: #00D4FF !important; }
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #1A1C23, #111318);
        border: 1px solid rgba(0, 212, 255, 0.2);
        padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif; font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00D4FF, #9B4DCA);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- CACHING FUNCTION ---
# Caches user data for 60 seconds to improve dashboard performance
@st.cache_data(ttl=60)
def get_cached_transactions(username):
    return get_transactions(username)

# ==========================================
# AUTHENTICATION GATEWAY
# ==========================================
if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <h1 style="margin-bottom: 0;">⚡ FINBOT CORE</h1>
                <p style="color: #00D4FF; font-weight: bold; letter-spacing: 1.5px;">SECURE ACCESS TERMINAL</p>
            </div>
        """, unsafe_allow_html=True)
        
        auth_container = st.container(border=True)
        with auth_container:
            tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
            
            with tab1:
                log_user = st.text_input("USERNAME", placeholder="Enter your username", key="log_user")
                log_pass = st.text_input("PASSWORD", type="password", placeholder="••••••••", key="log_pass")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("INITIALIZE SESSION", use_container_width=True):
                    if verify_user(log_user, log_pass):
                        st.session_state.logged_in = True
                        st.session_state.username = log_user
                        st.success("Access Granted. Loading Core...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Authentication Failed: Invalid Credentials")
                        
            with tab2:
                new_user = st.text_input("NEW USERNAME", placeholder="Choose a unique ID", key="new_user")
                new_pass = st.text_input("NEW PASSWORD", type="password", placeholder="Create a strong password", key="new_pass")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("CREATE SECURE ACCOUNT", use_container_width=True):
                    if new_user and new_pass:
                        if create_user(new_user, new_pass):
                            st.success("Identity Created! Switching to Login tab...")
                            time.sleep(1.5)
                        else:
                            st.error("Error: Username already exists in database.")
                    else:
                        st.warning("All fields are required for registration.")
    st.stop() 

# ==========================================
# MAIN SECURE APPLICATION
# ==========================================
with st.sidebar:
    st.header(f"👤 User: {st.session_state.username}")
    st.markdown("---")
    budget = st.slider("Monthly Budget Goal (₹)", 1000, 50000, 10000, step=500)
    
    st.markdown("---")
    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

st.title("FINBOT DASHBOARD")
st.caption("AUTONOMOUS NLP FINANCIAL TRACKING SYSTEM")
st.markdown("---")

placeholder = st.empty()

def update_dashboard():
    # Calling the cached dataset rather than pinging the DB every time
    df = get_cached_transactions(st.session_state.username) 
    with placeholder.container():
        if not df.empty:
            total_spent = df['amount'].sum()
            budget_percent = (total_spent / budget) * 100
            
            st.markdown(f"### 🎯 BUDGET UTILIZATION: {round(budget_percent)}%")
            st.progress(min(budget_percent / 100, 1.0))
            
            if budget_percent > 100:
                st.error(f"🚨 CRITICAL ALERT: Budget Exceeded by ₹{total_spent - budget:,.2f}!")
            st.markdown("---")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("💰 TOTAL SPEND", f"₹{total_spent:,.0f}")
            m2.metric("💳 TRANSACTIONS", len(df))
            m3.metric("🛒 LAST PURCHASE", df.iloc[-1]['item'])
            m4.metric("📉 REMAINING", f"₹{max(budget - total_spent, 0):,.0f}")

            c1, c2 = st.columns([2, 1])
            with c1:
                daily_trend = df.groupby('date')['amount'].sum().reset_index()
                fig_line = px.line(daily_trend, x='date', y='amount', title="Spending Timeline", markers=True)
                fig_line.update_traces(line_color='#00D4FF', line_width=4)
                fig_line.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_line, use_container_width=True) 
            
            with c2:
                fig_pie = px.pie(df, values='amount', names='category', hole=0.6, title="Category Distribution", color_discrete_sequence=px.colors.sequential.Agsunset)
                fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("SYSTEM READY. AWAITING INPUT.")

update_dashboard()

st.markdown("<br>", unsafe_allow_html=True)
if prompt := st.chat_input("Enter command... (e.g., 'Spent 4500 on piza')"):
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        with st.status("⚙️ NLP Engine Processing...", expanded=True) as status:
            time.sleep(0.5)
            data = process_text(prompt)
            
            if data["valid"]:
                add_transaction(st.session_state.username, data["item"], data["category"], data["amount"])
                # We MUST clear the cache here so the new transaction immediately shows up
                get_cached_transactions.clear() 
                
                status.update(label="Transaction Logged", state="complete", expanded=False)
                update_dashboard()
                st.success(f"Confirmed: ₹{data['amount']} debited for {data['item']}")
            else:
                status.update(label="Parsing Failed", state="error")
                st.error("❌ Command not recognized. Ensure you include a number.")