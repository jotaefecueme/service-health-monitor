import streamlit as st
import requests
from datetime import datetime
import time

SERVICE_URL = "https://dynamic-classifier.onrender.com/health"
TIMEOUT = 5

st.set_page_config(page_title="Estado del Servicio", page_icon="🩺")

st.title("🛡️ Monitor de Servicio")
st.markdown(f"### ⏱️ Última comprobación: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
st.markdown(f"Verificando el estado de: `{SERVICE_URL}`")
st.divider()

try:
    start = time.time()
    response = requests.get(SERVICE_URL, timeout=TIMEOUT)
    elapsed = time.time() - start

    st.write(f"⏳ Tiempo de respuesta: `{elapsed:.2f}` segundos")
    st.write(f"📦 Código de estado: `{response.status_code}`")

    if response.status_code == 200:
        st.success("✅ El servicio está EN LÍNEA.")
    else:
        st.warning("⚠️ El servicio respondió, pero con errores.")

    try:
        json_data = response.json()
        st.json(json_data)
    except ValueError:
        st.info("ℹ️ La respuesta no contenía JSON válido.")

except requests.exceptions.RequestException as e:
    st.error("❌ El servicio está CAÍDO.")
    st.code(str(e), language="text")
