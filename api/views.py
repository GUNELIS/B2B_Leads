from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from companies.models import Company
from leads.models import Lead, LeadCompanyMatch

from .serializers import (
    CompanySerializer,
    LeadCompanyMatchIn,
    LeadCompanyMatchReportSerializer,
    LeadCompanyMatchSerializer,
    LeadSerializer,
)


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


@api_view(["POST"])
def ingest_matches(request):
    """
    Accepts a list of match rows and writes them to LeadCompanyMatch.
    Expected body: {"matches":[{"lead_id":..,"company_id":..,"compatibility_score":..}, ...]}
    """
    items = request.data.get("matches", [])
    if not items:
        return Response({"created": 0, "detail": "No matches provided"}, status=400)

    created = []
    for row in items:
        s = LeadCompanyMatchIn(data=row)
        if not s.is_valid():
            continue
        d = s.validated_data
        try:
            lead = Lead.objects.get(pk=d["lead_id"])
            company = Company.objects.get(pk=d["company_id"])
        except (Lead.DoesNotExist, Company.DoesNotExist):
            continue
        created.append(
            LeadCompanyMatch(
                lead=lead,
                company=company,
                compatibility_score=d["compatibility_score"],
                matched_at=timezone.now(),
            )
        )

    if created:
        LeadCompanyMatch.objects.bulk_create(created, ignore_conflicts=True)

    return Response({"created": len(created)})


class LeadCompanyMatchReportView(generics.ListAPIView):
    queryset = LeadCompanyMatch.objects.select_related("lead", "company").all()
    serializer_class = LeadCompanyMatchReportSerializer
