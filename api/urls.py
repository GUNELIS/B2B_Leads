from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet,
    LeadViewSet,
    LeadCompanyMatchViewSet,
    LeadsToCleanView,
)

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"leads", LeadViewSet)
router.register(r"matches", LeadCompanyMatchViewSet)

urlpatterns = [
    path("leads/to-clean/", LeadsToCleanView.as_view(), name="leads-to-clean"),
    path("", include(router.urls)),
]
