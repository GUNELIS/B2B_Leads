from django.db import models

from companies.models import Company


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("qualified", "Qualified"),
        ("disqualified", "Disqualified"),
        ("converted", "Converted"),
    ]

    SOURCE_CHOICES = [
        ("web", "Website"),
        ("event", "Event"),
        ("referral", "Referral"),
        ("list", "Purchased/List"),
    ]

    first_name = models.CharField(max_length=100, help_text="Lead's first name")
    last_name = models.CharField(max_length=100, help_text="Lead's last name")
    email = models.EmailField(
        unique=True, help_text="Primary email address (must be unique)"
    )
    phone = models.CharField(
        max_length=50, blank=True, help_text="Phone number or mobile"
    )
    job_title = models.CharField(
        max_length=120, blank=True, help_text="Current job title or position"
    )

    industry_raw = models.CharField(
        max_length=100, blank=True, help_text="Industry as provided by lead"
    )
    region = models.CharField(
        max_length=100, blank=True, help_text="Geographic region or location"
    )
    interest_area = models.CharField(
        max_length=120, blank=True, help_text="Area of business interest"
    )
    rough_budget_raw = models.CharField(
        max_length=100, blank=True, help_text="Budget as originally provided"
    )
    rough_budget_normalized_euro = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Budget converted to EUR for comparison",
    )

    first_contacted_raw = models.CharField(
        max_length=100, blank=True, help_text="Original contact date/time as provided"
    )
    first_contacted_at = models.DateTimeField(
        null=True, blank=True, help_text="Parsed first contact timestamp"
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="web",
        help_text="How the lead was acquired",
    )
    consent_given = models.BooleanField(
        default=False, help_text="Whether lead has given marketing consent"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        help_text="Current lead qualification status",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When this lead was first created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Last modification timestamp"
    )

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["region"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.industry_raw}>"


class LeadCompanyMatch(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, help_text="The lead being matched"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, help_text="The company being matched"
    )
    compatibility_score = models.FloatField(
        help_text="Numerical compatibility score (0.0-1.0)"
    )
    matched_at = models.DateTimeField(
        auto_now_add=True, help_text="When this match was created"
    )

    class Meta:
        unique_together = ("lead", "company")
        indexes = [models.Index(fields=["compatibility_score"])]
        verbose_name = "Lead-Company Match"
        verbose_name_plural = "Lead-Company matches"

    def __str__(self):
        return f"{self.lead} ↔ {self.company} ({self.compatibility_score:.2f})"
