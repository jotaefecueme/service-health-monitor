import streamlit as st
import requests
import time
from datetime import datetime

# ---------------- Configuration ----------------
# Servicios predefinidos en el código
SERVICES = {
    "Classifier Health": "https://dynamic-classifier.onrender.com/health"
}

# ---------------- Caching ----------------
@st.cache_data(ttl=60)
def fetch_health(url, timeout=10):
    """
    Realiza una solicitud GET al endpoint de salud y devuelve el código de estado, el tiempo de respuesta.
    """
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start
        return response.status_code, round(elapsed, 2)
    except requests.RequestException as e:
        return None, str(e)

# ---------------- Sidebar ----------------
st.set_page_config(page_title="Monitor de Servicios", page_icon="🛡️")

st.sidebar.title("Configuración de Servicios")

# Control de intervalo de actualización
update_interval = st.sidebar.number_input(
    "Intervalo de actualización (segundos)", min_value=10, max_value=3600, value=30, step=10
)

# ---------------- Main Dashboard ----------------
st.title("🛡️ Monitor de Estado de Servicios")

# Obtener los resultados de la última comprobación desde la sesión (si existen)
if 'results' not in st.session_state:
    st.session_state.results = []

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

# Mostrar resultados de los servicios
for res in st.session_state.results:
    st.subheader(f"{res['Service']} - {res['Status']}")
    st.write(f"**URL**: {res['URL']}")
    st.write(f"**Código HTTP**: {res['HTTP Code']}")
    st.write(f"**Tiempo de Respuesta**: {res['Response Time (s)']} segundos")
    st.write(f"**Última Comprobación**: {res['Timestamp']}")
    if res['Status'] == 'DOWN':
        st.error(f"Error: {res['Error']}")
    st.divider()

# ---------------- Auto-refresh ----------------
st.write(f"Próxima actualización en {update_interval} segundos...")
time.sleep(update_interval)
st.rerun()
