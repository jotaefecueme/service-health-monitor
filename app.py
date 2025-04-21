import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------- Configuration ----------------
SERVICES = {
    "Classifier Health": "https://dynamic-classifier.onrender.com/health"
}

MAX_HISTORY = 5  # Número de checks que se mantienen en historial por servicio

# ---------------- Caching ----------------
@st.cache_data(ttl=60)
def fetch_health(url, timeout=10):
    try:
        start = datetime.now()
        response = requests.get(url, timeout=timeout)
        elapsed = (datetime.now() - start).total_seconds()
        return response.status_code, round(elapsed, 2), None
    except requests.RequestException as e:
        return None, None, str(e)

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Service Monitor", page_icon="🛡️")

# ---------------- Sidebar ----------------
st.sidebar.title("Service Configuration")
update_interval = st.sidebar.number_input(
    "Update interval (seconds)", min_value=10, max_value=3600, value=30, step=10
)

# ---------------- Auto-refresh ----------------
st_autorefresh(interval=update_interval * 1000, key="auto-refresh")

# ---------------- Session State Init ----------------
if "results" not in st.session_state:
    st.session_state.results = {}

# ---------------- Main Content ----------------
st.title("🛡️ Service Status Monitor")

for name, url in SERVICES.items():
    code, resp_time, error = fetch_health(url)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "UP" if code == 200 else "DOWN"

    result = {
        "Timestamp": timestamp,
        "Status": status,
        "HTTP Code": code if code else "Error",
        "Response Time (s)": resp_time if resp_time else "N/A",
        "Error": error if status == "DOWN" else ""
    }

    # Guardar histórico
    if name not in st.session_state.results:
        st.session_state.results[name] = []
    st.session_state.results[name].append(result)
    st.session_state.results[name] = st.session_state.results[name][-MAX_HISTORY:]

# ---------------- Visualización ----------------
for name, history in st.session_state.results.items():
    latest = history[-1]
    status_icon = "🟢" if latest["Status"] == "UP" else "🔴"

    st.markdown(f"### {status_icon} {name} — {latest['Status']}")
    st.metric("Response Time", f"{latest['Response Time (s)']} s")
    st.metric("HTTP Code", latest['HTTP Code'])
    st.write(f"**Last Checked**: {latest['Timestamp']}")
    
    if latest['Status'] == 'DOWN' and latest['Error']:
        st.error(f"Error: {latest['Error']}")

    st.divider()

st.write(f"⏱️ Auto-refresh cada {update_interval} segundos.")
