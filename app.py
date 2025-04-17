import streamlit as st
import requests
import time
from datetime import datetime

# ---------------- Configuration ----------------
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

# ---------------- Check session state for results ----------------
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
    # Save result in session state
    st.session_state.results = [result]  # This will replace the old results with new ones

# ---------------- Replace the placeholder content with the current data ----------------
with status_placeholder.container():
    for res in st.session_state.results:
        if res['Status'] == 'UP':
            # If the service is UP, display with a green background
            st.markdown(f"""
                <div style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;">
                    <h3>{res['Service']} - {res['Status']}</h3>
                    <p><strong>URL</strong>: {res['URL']}</p>
                    <p><strong>HTTP Code</strong>: {res['HTTP Code']}</p>
                    <p><strong>Response Time</strong>: {res['Response Time (s)']} seconds</p>
                    <p><strong>Last Checked</strong>: {res['Timestamp']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # If the service is DOWN, display with an error message in red
            st.error(f"{res['Service']} - {res['Status']}")
            st.write(f"**URL**: {res['URL']}")
            st.write(f"**HTTP Code**: {res['HTTP Code']}")
            st.write(f"**Response Time**: {res['Response Time (s)']} seconds")
            st.write(f"**Last Checked**: {res['Timestamp']}")
            st.write(f"Error: {res['Error']}")
        st.divider()

# ---------------- Auto-refresh ----------------
st.write(f"Next update in {update_interval} seconds...")
time.sleep(update_interval)

# Re-run the app to update
status_placeholder.empty()  # Empty the placeholder before rerunning the page
st.rerun()  # Rerun the app to refresh the content
