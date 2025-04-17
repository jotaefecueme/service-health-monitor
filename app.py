import streamlit as st
import requests

SERVICE_URL = "https://dynamic-classifier.onrender.com/health"

st.set_page_config(page_title="Estado del Servicio", page_icon="🩺")

st.title("🛡️ Monitor de Servicio")
st.write(f"Verificando el estado de: `{SERVICE_URL}`")

try:
    response = requests.get(SERVICE_URL, timeout=5)
    if response.status_code == 200:
        st.success("✅ El servicio está EN LÍNEA.")
    else:
        st.warning(f"⚠️ El servicio respondió con código {response.status_code}.")
except requests.exceptions.RequestException as e:
    st.error(f"❌ El servicio está CAÍDO. Detalles: {e}")
