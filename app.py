import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime

# ---------------- Configuration ----------------
DEFAULT_SERVICES = {
    "Classifier Health": "https://dynamic-classifier.onrender.com/health"
}

# ---------------- Caching ----------------
@st.cache_data(ttl=60)
def fetch_health(url, timeout=10):
    """
    Perform a GET request to the health endpoint and return status_code, response_time, and JSON if any.
    """
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start
        try:
            data = response.json()
        except ValueError:
            data = None
        return response.status_code, round(elapsed, 2), data, None
    except requests.RequestException as e:
        return None, None, None, str(e)

# ---------------- Sidebar ----------------
st.set_page_config(page_title="Service Monitor Dashboard", layout="wide", page_icon="🛡️")
st.sidebar.title("Settings")

# Allow user to configure services
services = st.sidebar.text_area(
    "Service URLs (one per line, label|url):",
    value="\n".join([f"{k}|{v}" for k, v in DEFAULT_SERVICES.items()]),
    height=200
)

# Parse services input
service_dict = {}
for line in services.splitlines():
    if '|' in line:
        label, url = line.split('|', 1)
        service_dict[label.strip()] = url.strip()

# Control update interval
update_interval = st.sidebar.number_input(
    "Update interval (seconds)", min_value=10, max_value=3600, value=30, step=10
)

# ---------------- Main Dashboard ----------------
st.title("🛡️ Service Monitor Dashboard")

# Tabs for organization
tabs = st.tabs(["Overview", "History"])

# Session State for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Fetch and collect data
results = []
for name, url in service_dict.items():
    code, resp_time, json_data, error = fetch_health(url)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'UP' if code == 200 else 'DOWN'
    results.append({
        'Service': name,
        'URL': url,
        'Timestamp': timestamp,
        'Status': status,
        'HTTP Code': code if code else 'Error',
        'Response Time (s)': resp_time if resp_time else 'N/A',
        'Error': error
    })
    # Append to history
    st.session_state.history.append(results[-1])

# Overview Tab
with tabs[0]:
    st.subheader("Real-time Status")
    cols = st.columns(len(results))
    for idx, res in enumerate(results):
        with cols[idx]:
            if res['Status'] == 'UP':
                st.success(f"{res['Service']}\n{res['HTTP Code']} | {res['Response Time (s)']}s")
            else:
                st.error(f"{res['Service']}\n{res['Error'] or res['HTTP Code']}")
            st.caption(res['Timestamp'])

    st.divider()
    st.write(f"Next update in {update_interval} seconds...")

# History Tab
with tabs[1]:
    st.subheader("Response History")
    df = pd.DataFrame(st.session_state.history)
    st.data_editor(df, use_container_width=True)

    # Plot response times for each service
    st.subheader("Response Time Trends")
    for name in service_dict.keys():
        df_srv = df[df['Service'] == name]
        if not df_srv.empty:
            chart = df_srv.set_index('Timestamp')['Response Time (s)']
            st.line_chart(chart, height=200)

# Auto-refresh
st.write("_This dashboard auto-refreshes based on the selected interval._")
time.sleep(update_interval)
st.rerun()
