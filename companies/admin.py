from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "industry",
        "sector",
        "region",
        "typical_project_budget_euro",
        "created_at",
    )
    search_fields = ("name", "industry", "region")
    list_filter = ("industry", "region")
    fields = (
        "name",
        "website",
        "sector",
        "industry",
        "region",
        "typical_project_budget_euro",
        "tech_stack",
        "notes",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")
