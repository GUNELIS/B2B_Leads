"B2B Leads" Changelog
======================

All notable changes to B2B leads project are documented
in this file.

_The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)._


0.5.0 (unreleased)
------------------
### Major features

### Added
- Reporting Agent service:
- New FastAPI microservice to fetch top LeadCompanyMatch records, analyze trends, and generate a textual report.
- Initial scaffold: /health and /generate-report endpoints, HTTP client stub, analysis and summarizer placeholders.
- Dockerfile and requirements for CPU-only lightweight LLMs (transformers + torch).
- Compose integration exposing port 8100 with environment-configurable Django base URL and endpoint paths.

### Changed
- Added concise docstrings across Reporting Agent modules (main.py, client.py, analysis.py, summarizer.py) to clarify responsibilities, inputs, and outputs.

### Deprecated
_No changes._

### Removed
_No changes._

### Fixed
_No changes._

### Security
- Optional bearer DJANGO_API_KEY header support for inter-service calls.

0.4.0 (unreleased)
------------------
### Major features
- Implemented Agent 2 (Scoring Agent) as an independent FastAPI microservice for predictive lead–company matching.
- Completed full multi-agent integration: Django (data source) → Cleaning Agent → Scoring Agent → Django (matches).

### Added
- Scoring Agent service:
    - Built with FastAPI, exposing /ingest-cleaned-leads, /ingest-companies, /train, /evaluate, /score, /forward-scored-leads, and /health endpoints.
    - Integrated scikit-learn logistic regression model to estimate compatibility_score between leads and companies.
    - Introduced in-memory store for quick iteration (leads and companies held in memory).
    - Added model serialization and evaluation metrics reporting.
    - Extended Docker Compose with scoring_agent container on port 8090, including health checks.
- Added schema definitions (schemas.py) for validated request and response bodies using Pydantic.
- Added train.py for model training pipeline, including probabilistic label generation, feature encoding, and accuracy scoring.
- Added model.py for model persistence and inference.
- Added storage.py as a lightweight in-memory data store with thread safety.
- Added complete REST testing coverage with Postman-compatible payloads for leads and companies.
- Added forwarding integration: /forward-scored-leads endpoint posts model results back to Django via REST API to populate LeadCompanyMatch.

### Changed
- Enhanced Cleaning Agent and Django interaction assumptions to support downstream persistence.
- Updated Docker Compose network to allow cross-service communication between Django, Cleaning Agent, and Scoring Agent.
- Adjusted example payloads and documentation to reflect normalized fields (industry, budget_normalized_euro, region, etc.).
- Added docstrings and code documentation across train.py for clarity and maintainability.

### Deprecated
_No changes._

### Removed
_No changes._

### Fixed
- Corrected label generation logic to avoid 0/1 saturation and enable more realistic probability outputs.
- Fixed sorting and ranking logic in /score to ensure descending order of best matches per lead.

### Security
- Added configurable environment variables for Django endpoint URLs and optional API key headers for inter-agent communication.

0.3.0 (unreleased)
------------------
### Major features
- Added a standalone Cleaning Agent microservice (FastAPI-based) to normalize and prepare raw leads from the Django app.

### Added
- Created new cleaning_agent/ directory with Dockerized FastAPI app.
- Added /health and /clean-leads endpoints in app/main.py.
- Implemented REST client (app/rest_client.py) to fetch raw leads from Django API /api/leads/to-clean/.
- Implemented lead cleaning logic (app/cleaner.py) to normalize:
    - Budgets (varied currency formats and symbols).
    - Dates (multiple formats).
    - Phone numbers (E.164 normalization).
    - Regions and industries (canonical mapping and fuzzy matching).
- Added .env and requirements.txt for dependency management.
- Updated docker-compose.yml to include cleaning_agent service with environment variable DJANGO_API_BASE.
- Added a README.md describing structure, setup, environment variables, and usage instructions.
- Added pytest-based test suite in app/tests/test_cleaner.py covering core normalization functions.

### Changed
- Extended Django API routes with /api/leads/to-clean/ endpoint (LeadsToCleanView) to provide filtered leads for cleaning agent.
- Adjusted router order in api/urls.py to ensure /api/leads/to-clean/ takes precedence over DRF viewset routes.
- Updated cleaning agent main route to handle both GET and POST methods for easier testing (browser and Postman).

### Deprecated
_No changes._

### Removed
_No changes._

### Fixed
- Fixed 404 and routing conflicts in Django API by reordering urlpatterns.
- Fixed DisallowedHost errors by updating Django ALLOWED_HOSTS to include container service name (django).

### Security
_No changes._


0.2.0 (unreleased)
------------------
### Major features
- Containerized the Django application and established a multi-service Docker Compose setup to support future microservices (e.g. Cleaning Agent).

### Added
- Created Dockerfile for Django app with Python 3.11 base, environment setup, and runserver command.
- Added .dockerignore to exclude cache, environment files, virtual environments, and development artifacts.
- Added docker-compose.yml with two services:
    - django: Builds from local context, runs Django development server on port 8000, and mounts project source code.
    - cleaning_agent: Placeholder service running a Python 3.11 container with mapped directory for later development.
- Configured volume mounts to allow live code reloading for local development.
- Set up default environment variable DEBUG=1 in Django container.

### Changed
- Simplified docker-compose.yml by removing unnecessary dependency link (depends_on) between Django and cleaning_agent.
- Clarified container code paths (/app for Django and /cleaning_agent for cleaning_agent).

### Deprecated
_No changes._

### Removed
_No changes._

### Fixed
_No changes._

### Security
_No changes._


0.1.0 (unreleased)
------------------
### Major features
- Introduced LeadCompanyMatch model to manage many-to-many relationships between leads and companies with scoring support.

### Added
- Added LeadCompanyMatch model with fields: lead, company, score, and matched_at.
- Added DRF LeadCompanyMatchViewSet and routes under /api/matches/.
- Added API router registration for companies, leads, and matches in api/urls.py.
- Added browsable DRF API accessible via /api/.

### Changed
- Removed the direct ForeignKey from Lead to Company; replaced with LeadCompanyMatch.
- Moved compatibility_score from Lead to LeadCompanyMatch for cleaner model separation.
- Updated core/urls.py to include path('api/', include('api.urls')).
- Updated serializers and views to align with new schema.

### Deprecated
_No changes._

### Removed
- Removed headcount field from Company as it was redundant for current scoring logic.

### Fixed
- Fixed django.core.exceptions.ImproperlyConfigured error by adding valid urlpatterns in api/urls.py.

### Security
_No changes._
