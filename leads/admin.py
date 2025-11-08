from django.contrib import admin

from .models import Lead, LeadCompanyMatch


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "job_title",
        "status",
        "region",
        "interest_area",
        "rough_budget_raw",
        "source",
        "consent_given",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "source", "consent_given", "created_at")
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "job_title",
        "industry_raw",
    )
    ordering = ("-created_at",)
    fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "job_title",
        "industry_raw",
        "region",
        "interest_area",
        "rough_budget_raw",
        "rough_budget_normalized_euro",
        "first_contacted_raw",
        "first_contacted_at",
        "status",
        "source",
        "consent_given",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at", "first_contacted_at")


@admin.register(LeadCompanyMatch)
class LeadCompanyMatchAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "company",
        "compatibility_score",
        "matched_at",
    )
    search_fields = ("lead__first_name", "lead__last_name", "company")
    ordering = ("-matched_at",)
    fields = (
        "lead",
        "company",
        "compatibility_score",
        "matched_at",
    )
    readonly_fields = ("matched_at",)
