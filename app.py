import streamlit as st
import requests
import time
from datetime import datetime

# ---------------- Configuration ----------------
# Predefined services in the code
SERVICES = {
    "Classifier Health": "https://dynamic-classifier.onrender.com/health"
}

# ---------------- Caching ----------------
@st.cache_data(ttl=60)
def fetch_health(url, timeout=10):
    """
    Perform a GET request to the health endpoint and return the status code, response time.
    """
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start
        return response.status_code, round(elapsed, 2)
    except requests.RequestException as e:
        return None, str(e)

# ---------------- Sidebar ----------------
st.set_page_config(page_title="Service Monitor", page_icon="🛡️")

st.sidebar.title("Service Configuration")

# Control the update interval
update_interval = st.sidebar.number_input(
    "Update interval (seconds)", min_value=10, max_value=3600, value=30, step=10
)

# ---------------- Main Dashboard ----------------
st.title("🛡️ Service Status Monitor")

# Get the results of the last check from the session (if they exist)
if 'results' not in st.session_state:
    st.session_state.results = []

# ---------------- Create an empty placeholder for dynamic content ----------------
status_placeholder = st.empty()

# Fetch and collect data
for name, url in SERVICES.items():
    code, resp_time = fetch_health(url)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'UP' if code == 200 else 'DOWN'
    result = {
        'Service': name,
        'URL': url,
        'Timestamp': timestamp,
        'Status': status,
        'HTTP Code': code if code else 'Error',
        'Response Time (s)': resp_time if resp_time else 'N/A',
        'Error': resp_time if code != 200 else ''
    }
    st.session_state.results.append(result)

# Display service results
with status_placeholder.container():  # This will ensure the content is replaced dynamically
    for res in st.session_state.results:
        st.subheader(f"{res['Service']} - {res['Status']}")
        st.write(f"**URL**: {res['URL']}")
        st.write(f"**HTTP Code**: {res['HTTP Code']}")
        st.write(f"**Response Time**: {res['Response Time (s)']} seconds")
        st.write(f"**Last Checked**: {res['Timestamp']}")
        if res['Status'] == 'DOWN':
            st.error(f"Error: {res['Error']}")
        st.divider()

# ---------------- Auto-refresh ----------------
st.write(f"Next update in {update_interval} seconds...")
time.sleep(update_interval)
status_placeholder.empty() 
st.rerun() 
