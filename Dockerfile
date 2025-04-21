FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 8000 10000

CMD ["sh", "-c", "uvicorn health_app:app --host 0.0.0.0 --port $PORT & streamlit run app.py --server.port $PORT"]
