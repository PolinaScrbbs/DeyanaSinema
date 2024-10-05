FROM python:3.11-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY .env ./
COPY config.py ./
COPY alembic.ini ./
COPY requirements.txt ./
COPY migrations/ ./migrations/
COPY api/ ./api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 5432

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000"]

