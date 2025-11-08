from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from companies.models import Company
from leads.models import Lead, LeadCompanyMatch

from .serializers import CompanySerializer, LeadCompanyMatchSerializer, LeadSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """API endpoint to view companies."""

    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanySerializer


class LeadViewSet(viewsets.ModelViewSet):
    """API endpoint to view leads."""

    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer


class LeadCompanyMatchViewSet(viewsets.ModelViewSet):
    """API endpoint to view lead-company matches."""

    queryset = LeadCompanyMatch.objects.all().order_by("-compatibility_score")
    serializer_class = LeadCompanyMatchSerializer


class LeadsToCleanView(APIView):
    """API endpoint to fetch leads that need cleaning."""

    def get(self, request):
        """Fetch leads with status 'new' that need cleaning."""
        limit = int(request.query_params.get("limit", 100))

        queryset = Lead.objects.filter(status="new").order_by("-created_at")[:limit]

        serializer = LeadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
