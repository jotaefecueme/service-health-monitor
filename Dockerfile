FROM python:3.9-slim

RUN apt-get update && apt-get install -y supervisor

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000 8501

CMD ["/usr/bin/supervisord"]
