FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Default envs (override in compose)
ENV DJANGO_BASE_URL=http://django:8000 \
    MATCHES_ENDPOINT=/api/matches/ \
    REPORT_TOP_N=50 \
    LLM_MODEL_NAME=distilgpt2 \
    TIMEOUT_SECONDS=15

EXPOSE 8100
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100"]
