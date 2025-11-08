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
