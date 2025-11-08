from rest_framework import viewsets

from companies.models import Company
from leads.models import Lead, LeadCompanyMatch

from .serializers import (CompanySerializer, LeadCompanyMatchSerializer,
                          LeadSerializer)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanySerializer


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer


class LeadCompanyMatchViewSet(viewsets.ModelViewSet):
    queryset = LeadCompanyMatch.objects.all().order_by("-compatibility_score")
    serializer_class = LeadCompanyMatchSerializer
