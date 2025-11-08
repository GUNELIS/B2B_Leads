# Cleaning Agent

A minimal FastAPI microservice that cleans and normalizes raw B2B leads from a Django app.

## Overview
- Fetches raw leads from the Django REST API (`/api/leads/to-clean/`).
- Normalizes fields: budgets, dates, phones, industries, and regions.
- Runs as its own container in Docker Compose.


## Usage
### Local run
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Check health:

```bash
curl http://localhost:8080/health
```

### Run test
```bash
docker-compose exec cleaning_agent pytest
```