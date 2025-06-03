FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8001

CMD ["python", "app/main.py"]

# Datenbank neu starten
# docker compose down -v && docker compose up -d

# Service starten
# python main.py

# Alle Note abrufen
# curl http://localhost:8000/notes/