from rest_framework import serializers

from companies.models import Company
from leads.models import Lead, LeadCompanyMatch


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"


class LeadCompanyMatchSerializer(serializers.ModelSerializer):
    lead_email = serializers.CharField(source="lead.email", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = LeadCompanyMatch
        fields = "__all__"


class LeadCompanyMatchIn(serializers.Serializer):
    lead_id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    compatibility_score = serializers.FloatField(min_value=0.0, max_value=1.0)

class LeadCompanyMatchReportSerializer(serializers.ModelSerializer):
    """Serializer exposing both lead and company context for reporting."""

    lead_email = serializers.CharField(source="lead.email", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    # From lead
    lead_industry = serializers.CharField(
        source="lead.industry_raw", read_only=True
    )
    lead_region = serializers.CharField(
        source="lead.region", read_only=True
    )
    lead_budget_normalized_euro = serializers.DecimalField(
        source="lead.rough_budget_normalized_euro",
        read_only=True,
        max_digits=12,
        decimal_places=2,
        allow_null=True,
    )

    # From company
    company_industry = serializers.CharField(
        source="company.industry", read_only=True
    )
    company_region = serializers.CharField(
        source="company.region", read_only=True
    )
    company_budget_normalized_euro = serializers.DecimalField(
        source="company.typical_project_budget_euro",
        read_only=True,
        max_digits=12,
        decimal_places=2,
        allow_null=True,
    )

    # Uniform score alias for reporting_agent
    score = serializers.FloatField(source="compatibility_score", read_only=True)

    class Meta:
        model = LeadCompanyMatch
        fields = [
            "id",
            "lead_email",
            "company_name",
            "score",
            "lead_industry",
            "lead_region",
            "lead_budget_normalized_euro",
            "company_industry",
            "company_region",
            "company_budget_normalized_euro",
            "matched_at",
        ]