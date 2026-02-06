import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration for wide layout
st.set_page_config(page_title="Scrappy Market AI", layout="wide")

# --- LEFT SIDEBAR: Chat History & Data Resources ---
with st.sidebar:
    st.title("📂 Scrappy Market")
    
    # Upper Section: Chat History
    st.subheader("Chat History")
    chat_history = ["Supplier Performance Review", "Inventory Shortage Store 10", "Seasonal Trend Analysis"]
    st.radio("Select a session:", chat_history, label_visibility="collapsed")
    
    st.divider() 
    
    # Lower Section: Database Resources
    st.subheader("Available Resources")
    tables = ["Suppliers (Gold)", "Procurement_Orders (Silver)", "Product_Catalog (Bronze)"]
    st.multiselect("Active Tables:", tables, default=tables[0])

# --- MAIN LAYOUT: Center (Chat & Results) and Right Sidebar (Reasoning) ---
# Adjusting column ratios: [Center: 3, Right: 1]
col_main, col_reasoning = st.columns([3, 1])

with col_main:
    # UPPER SECTION: Chat Interface
    st.header("💬 Chat: Supplier Performance Review")
    
    # Scrollable chat container
    chat_window = st.container(height=350)
    with chat_window:
        st.chat_message("user").write("Show me the top 5 suppliers by reliability score for the last quarter.")
        st.chat_message("assistant").write("Analyzing procurement logs and supplier ratings... Please hold on.")

    # Chat input bar
    if prompt := st.chat_input("Ask Scrappy Market..."):
        st.chat_message("user").write(prompt)

    st.divider()

    # LOWER SECTION: Last Query Results (Suppliers Table Example)
    st.subheader("📊 Last Query Results: Top Suppliers")
    
    # Mock data for Suppliers Table
    supplier_data = {
        'supplier_id': ['SUP-001', 'SUP-042', 'SUP-109', 'SUP-015', 'SUP-088'],
        'supplier_name': ['Global Logistics Inc', 'Fresh Farms Co', 'TechRetail Solutions', 'Prime Goods Ltd', 'EcoPack Systems'],
        'reliability_score': [98.5, 96.2, 94.8, 92.1, 91.5],
        'last_delivery': ['2026-01-20', '2026-02-01', '2026-01-28', '2026-02-03', '2026-01-15'],
        'tier': ['Gold', 'Gold', 'Silver', 'Gold', 'Silver']
    }
    df_suppliers = pd.DataFrame(supplier_data)
    
    # Displaying the table
    st.dataframe(df_suppliers, use_container_width=True)

with col_reasoning:
    # RIGHT SIDEBAR: Connection Info & Reasoning Path
    
    # Upper Section (Smaller): Connection Status
    with st.container(border=True):
        st.markdown("### 🌐 Connection")
        st.caption("**DB:** MySQL - Tier 1")
        st.caption("**Status:** 🟢 Online")
        st.caption(f"**Uptime:** {datetime.now().strftime('%H:%M')} EST")

    # Lower Section (Larger): Reasoning Path & SQL
    st.subheader("🧠 Reasoning Path")
    
    # Using a larger status container for logs
    with st.status("Agent Investigation Logs", expanded=True):
        st.write("🔍 **Intent Agent:** Classified as *Supplier Analysis*")
        st.write("📋 **Planner:** Searching *Suppliers* and *Procurement* tables")
        st.write("🔗 **Lineage:** Mapping reliability metrics to Q4 2025")
        st.write("✍️ **Query Builder:** Writing SQL for Tier 1 Gold data")
        
    st.divider()
    
    st.subheader("📜 Generated SQL")
    sql_query = """
SELECT supplier_id, supplier_name, reliability_score 
FROM Suppliers 
WHERE tier = 'Gold' 
ORDER BY reliability_score DESC 
LIMIT 5;
    """
    st.code(sql_query, language="sql")