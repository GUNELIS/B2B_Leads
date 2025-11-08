from django.db import models


class Company(models.Model):
    name = models.CharField(
        max_length=200, unique=True, help_text="Company name (must be unique)"
    )
    website = models.URLField(blank=True, help_text="Company website URL")
    sector = models.CharField(
        max_length=100,
        blank=True,
        help_text="Business sector (e.g., 'finance', 'healthcare')",
    )
    industry = models.CharField(
        max_length=100,
        blank=True,
        help_text="Industry sector (e.g., 'SaaS', 'manufacturing')",
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        help_text="Geographic region (e.g., 'EMEA', 'DACH', 'North America')",
    )
    typical_project_budget_euro = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Typical project budget in euros",
    )
    tech_stack = models.JSONField(
        default=list,
        blank=True,
        help_text="List of technologies used (e.g., ['aws', 'snowflake', 'salesforce'])",
    )
    notes = models.TextField(blank=True, help_text="Additional notes about the company")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the record was last updated"
    )

    class Meta:
        indexes = [
            models.Index(fields=["industry"]),
            models.Index(fields=["region"]),
        ]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
