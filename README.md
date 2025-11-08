# B2B_Leads
A simple lead acquisition pipeline with Django as a core web app.
Developed by Ben Hasenson.

## Quickstart (Windows)

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Apps

<h3>Companies:</h3> 
Company metadata that informs compatibility scoring (industry, region, headcount, stack).

<h3>Leads:</h3> 
Individual contacts and their raw, noisy fields plus normalized targets.

<h3>API:</h3> 
django rest framework viewsets and routing for quick CRUD.

API endpoints:

- GET /api/companies/

- GET /api/leads/

## Uploading fixture data to the DB

In this project we have some sample data in json fixtures. To upload them to the database, do the following:

```bat
python manage.py loaddata <my-fixture-name>.json
```