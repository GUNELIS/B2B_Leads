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

## Example to test the API (e.g. in POSTMAN)

POST http://localhost:8090/ingest-cleaned-leads
Body: 
{
  "leads": [
    {"id":1,"first_name":"Lena","last_name":"Klein","industry":"FinTech","region":"EMEA","interest_area":"automation","budget_normalized_euro":12000},
    {"id":2,"first_name":"Omar","last_name":"Ng","industry":"SaaS","region":"APAC","interest_area":"crm","budget_normalized_euro":25000},
    {"id":3,"first_name":"Sara","last_name":"Holt","industry":"Retail","region":"DACH","interest_area":"marketing","budget_normalized_euro":18000},
    {"id":4,"first_name":"Tomi","last_name":"Okafor","industry":"AI","region":"EMEA","interest_area":"analytics","budget_normalized_euro":40000},
    {"id":5,"first_name":"Yasmin","last_name":"Reed","industry":"Healthcare","region":"NA","interest_area":"data infra","budget_normalized_euro":35000},
    {"id":6,"first_name":"Igor","last_name":"Petrov","industry":"Manufacturing","region":"CEE","interest_area":"iot","budget_normalized_euro":21000},
    {"id":7,"first_name":"Clara","last_name":"Lopez","industry":"EdTech","region":"LATAM","interest_area":"platforms","budget_normalized_euro":8000},
    {"id":8,"first_name":"Jin","last_name":"Park","industry":"Gaming","region":"APAC","interest_area":"user growth","budget_normalized_euro":27000},
    {"id":9,"first_name":"Ben","last_name":"Thompson","industry":"Cybersecurity","region":"EMEA","interest_area":"risk","budget_normalized_euro":33000},
    {"id":10,"first_name":"Elina","last_name":"Zhou","industry":"FinTech","region":"NA","interest_area":"payments","budget_normalized_euro":42000},
    {"id":11,"first_name":"Ravi","last_name":"Desai","industry":"SaaS","region":"EMEA","interest_area":"ops","budget_normalized_euro":15000},
    {"id":12,"first_name":"Greta","last_name":"Jensen","industry":"AI","region":"DACH","interest_area":"data science","budget_normalized_euro":28000},
    {"id":13,"first_name":"Luis","last_name":"Martinez","industry":"Retail","region":"LATAM","interest_area":"ads","budget_normalized_euro":9500},
    {"id":14,"first_name":"Hana","last_name":"Ito","industry":"Healthcare","region":"APAC","interest_area":"clinical","budget_normalized_euro":37000},
    {"id":15,"first_name":"Mateo","last_name":"Silva","industry":"Gaming","region":"LATAM","interest_area":"monetization","budget_normalized_euro":26000},
    {"id":16,"first_name":"Zara","last_name":"Singh","industry":"Manufacturing","region":"EMEA","interest_area":"automation","budget_normalized_euro":30000},
    {"id":17,"first_name":"Noah","last_name":"Smith","industry":"Cybersecurity","region":"NA","interest_area":"compliance","budget_normalized_euro":44000},
    {"id":18,"first_name":"Eva","last_name":"Schmidt","industry":"EdTech","region":"DACH","interest_area":"learning","budget_normalized_euro":19000},
    {"id":19,"first_name":"Jonas","last_name":"Berg","industry":"AI","region":"EMEA","interest_area":"mlops","budget_normalized_euro":38000},
    {"id":20,"first_name":"Priya","last_name":"Kaur","industry":"SaaS","region":"NA","interest_area":"crm","budget_normalized_euro":26000}
  ]
}

POST http://localhost:8090/ingest-companies
Body:
[
  {"id":1,"name":"Paynova","industry":"FinTech","region":"EMEA","typical_project_budget_euro":15000},
  {"id":2,"name":"Cloudverse","industry":"SaaS","region":"NA","typical_project_budget_euro":30000},
  {"id":3,"name":"Shopium","industry":"Retail","region":"DACH","typical_project_budget_euro":25000},
  {"id":4,"name":"Mediscan","industry":"Healthcare","region":"APAC","typical_project_budget_euro":40000},
  {"id":5,"name":"AutoForge","industry":"Manufacturing","region":"CEE","typical_project_budget_euro":22000},
  {"id":6,"name":"Learnify","industry":"EdTech","region":"LATAM","typical_project_budget_euro":12000},
  {"id":7,"name":"GameSpark","industry":"Gaming","region":"APAC","typical_project_budget_euro":27000},
  {"id":8,"name":"SentraSec","industry":"Cybersecurity","region":"NA","typical_project_budget_euro":35000},
  {"id":9,"name":"Neurolytics","industry":"AI","region":"EMEA","typical_project_budget_euro":38000},
  {"id":10,"name":"OmniRetail","industry":"Retail","region":"LATAM","typical_project_budget_euro":15000}
]

POST http://localhost:8090/train
Body: []

POST http://localhost:8090/score
Body:
{
  "leads": [
    {
      "id": 1,
      "industry": "FinTech",
      "region": "EMEA",
      "budget_normalized_euro": 12000
    },
    {
      "id": 4,
      "industry": "AI",
      "region": "EMEA",
      "budget_normalized_euro": 40000
    },
    {
      "id": 14,
      "industry": "Healthcare",
      "region": "APAC",
      "budget_normalized_euro": 37000
    }
  ]
}
