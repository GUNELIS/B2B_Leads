from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CompanyViewSet,
    LeadCompanyMatchViewSet,
    LeadsToCleanView,
    LeadViewSet,
    ingest_matches,
    LeadCompanyMatchReportView,
)

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"leads", LeadViewSet)
router.register(r"matches", LeadCompanyMatchViewSet)

urlpatterns = [
    path("matches/report/", LeadCompanyMatchReportView.as_view(), name="matches-report"),
    path("leads/to-clean/", LeadsToCleanView.as_view(), name="leads-to-clean"),
    path("matches/ingest/", ingest_matches, name="matches-ingest"),
    path("", include(router.urls)),
]
