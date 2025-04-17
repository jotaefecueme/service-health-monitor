import streamlit as st
import requests
import time
from datetime import datetime

# ---------------- Configuration ----------------
SERVICE_URL = "https://dynamic-classifier.onrender.com/health"

# ---------------- Caching ----------------
@st.cache_data(ttl=60)
def fetch_health(url, timeout=10):
    """
    Perform a GET request to the health endpoint and return status_code, response_time.
    """
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start
        return response.status_code, round(elapsed, 2)
    except requests.RequestException as e:
        return None, str(e)

# ---------------- Main Dashboard ----------------
st.set_page_config(page_title="Service Health Monitor", page_icon="🛡️")

# Title of the dashboard
st.title("🛡️ Service Health Monitor")

# ---------------- Check Service Status ----------------
if 'last_check' not in st.session_state or time.time() - st.session_state.last_check > 60:
    # Fetch data if it's the first load or more than 60 seconds have passed
    code, resp_time = fetch_health(SERVICE_URL)
    st.session_state.last_check = time.time()  # Store the timestamp of the last check
    
    # Store the results in session state
    st.session_state.status_code = code
    st.session_state.response_time = resp_time

# ---------------- Display Status ----------------
if st.session_state.status_code == 200:
    st.success(f"✅ El servicio está **EN LÍNEA**.")
    st.write(f"⏱️ Último tiempo de respuesta: {st.session_state.response_time} segundos.")
else:
    st.error(f"❌ El servicio está **CAÍDO**. Error: {st.session_state.response_time}")

# Auto-refresh every minute (but without resetting the session state every time)
st.write("_This page refreshes every minute to check the service status._")
time.sleep(60)
st.experimental_rerun()
