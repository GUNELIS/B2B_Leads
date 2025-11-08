from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, LeadCompanyMatchViewSet, LeadViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"leads", LeadViewSet)
router.register(r"matches", LeadCompanyMatchViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
