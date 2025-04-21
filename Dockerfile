# Usar la imagen base
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los requisitos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puertos
EXPOSE 8501 8000 10000

# Definir el comando para iniciar ambos servicios
CMD ["sh", "-c", "uvicorn health_app:app --host 0.0.0.0 --port $PORT & streamlit run app.py --server.port $PORT"]
