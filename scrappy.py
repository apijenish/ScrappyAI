import streamlit as st
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="Scrappy Market AI", layout="wide")

# Initialize Session State for multiple chats
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

# --- SIDEBAR: Chat History & Management ---
with st.sidebar:
    st.title("🛠 Scrappy Panel")
    
    # 1. New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_id = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_chat_id] = []
        st.session_state.current_chat = new_chat_id
        st.rerun()

    st.divider()
    st.subheader("Recent Chats")
    
    # 2. Chat Selection Menu
    for chat_name in list(st.session_state.all_chats.keys()):
        if st.button(chat_name, key=chat_name, use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

# --- MAIN INTERFACE ---
st.title("🛒 Scrappy Market")
st.caption(f"Currently viewing: **{st.session_state.current_chat}**")

# Display historical messages for the selected chat
for message in st.session_state.all_chats[st.session_state.current_chat]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Enter your business question here..."):
    # Add user message to state
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Integrated Reasoning Path
    with st.chat_message("assistant"):
        with st.status("🔍 AI Agents are investigating...", expanded=True) as status:
            st.write("Checking user intent...")
            time.sleep(0.5)
            st.write("✔ **Intent Agent:** Classified as 'Sales Analysis'")
            
            st.write("Mapping data logic...")
            time.sleep(0.5)
            st.write("✔ **Planner Agent:** Strategy defined for Tier 1 Tables")
            
            st.write("Analyzing database schema...")
            time.sleep(0.5)
            st.write("✔ **Lineage Agent:** Columns 'Total_Sales' and 'Store_ID' identified")
            
            st.write("Generating optimized SQL...")
            time.sleep(0.5)
            st.write("✔ **Query Builder Agent:** SQL instruction finalized")
            status.update(label="Investigation Complete!", state="complete", expanded=False)

        # 4. Result Section
        st.markdown("### 📊 Query Results")
        mock_results = pd.DataFrame({
            'Store_ID': [512, 102, 305],
            'Total_Sales': ["$45,200", "$38,150", "$29,900"],
            'Performance': ["Above Target", "On Track", "Below Target"]
        })
        st.table(mock_results)

        with st.expander("View Generated SQL Query"):
            st.code("SELECT Store_ID, SUM(Sales) FROM Daily_Performance GROUP BY Store_ID;", language="sql")

    # Add assistant message to state
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": "Here are the results for your request."})