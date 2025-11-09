# Scoring Agent

FastAPI microservice that ingests cleaned leads, trains a model, evaluates, and scores.

## Run

docker build -t scoring_agent ./scoring_agent
docker run --rm -p 8090:8090 scoring_agent

Or via docker-compose (service: scoring_agent).

## Endpoints

GET  /health
POST /ingest-cleaned-leads
POST /train
GET  /evaluate
POST /score
POST /forward-scored-leads  # stub

## Example

POST /ingest-cleaned-leads
Body: {"leads":[{...}]}

POST /score
Body: {"leads":[{...}]}
