import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime

# Configuración del servicio
SERVICE_URL = "https://dynamic-classifier.onrender.com/health"
TIMEOUT = 5
UPDATE_INTERVAL = 30  # Cada cuánto tiempo se actualiza (en segundos)

# Configuración de Streamlit
st.set_page_config(page_title="Estado del Servicio", page_icon="🩺")
st.title("🛡️ Monitor de Servicio en Tiempo Real")

# Lista para almacenar el historial de respuestas
if 'history' not in st.session_state:
    st.session_state.history = []

# Función para realizar la comprobación
def check_service():
    try:
        start = time.time()
        response = requests.get(SERVICE_URL, timeout=TIMEOUT)
        elapsed = time.time() - start
        return response, elapsed
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Realizar la comprobación y actualizar el historial
response, elapsed = check_service()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Agregar el resultado al historial
if response:
    status_code = response.status_code
    response_json = response.json() if response.status_code == 200 else {}
else:
    status_code = "Error"
    response_json = {}

st.session_state.history.append({
    "timestamp": timestamp,
    "status_code": status_code,
    "response_time": f"{elapsed:.2f}s",
    "response_json": response_json
})

# Mostrar los resultados
st.write(f"⏱️ Última comprobación: `{timestamp}`")
st.write(f"⏳ Tiempo de respuesta: `{elapsed:.2f}` segundos")
st.write(f"📦 Código de estado: `{status_code}`")

if response and status_code == 200:
    st.success("✅ El servicio está EN LÍNEA.")
else:
    st.error("❌ El servicio está CAÍDO.")

# Mostrar la respuesta JSON
st.subheader("Respuesta JSON")
st.json(response_json)

# Mostrar historial en tabla
st.subheader("Historial de Respuestas")
df = pd.DataFrame(st.session_state.history)
st.dataframe(df)

# Gráfico de tiempos de respuesta
st.subheader("Gráfico de Tiempos de Respuesta")
df['response_time'] = df['response_time'].apply(lambda x: float(x.replace("s", "")))
st.line_chart(df[['timestamp', 'response_time']].set_index('timestamp'))

# Configuración de actualización automática
st.write(f"Actualización cada {UPDATE_INTERVAL} segundos")
time.sleep(UPDATE_INTERVAL)  # espera para que se recargue automáticamente
st.experimental_rerun()
