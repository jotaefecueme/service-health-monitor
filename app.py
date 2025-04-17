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

# Fetch and collect data
code, resp_time = fetch_health(SERVICE_URL)

# Display the status
if code == 200:
    st.success(f"✅ El servicio está **EN LÍNEA**.")
    st.write(f"⏱️ Último tiempo de respuesta: {resp_time} segundos.")
else:
    st.error(f"❌ El servicio está **CAÍDO**. Error: {resp_time}")

# Auto-refresh every minute
st.write("_This page refreshes every minute to check the service status._")
time.sleep(60)
st.experimental_rerun()
