from django.db import models
from django.conf import settings
import hashlib
from django.db import models
from django.conf import settings
class Case(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_cases'
    )
    assigned_investigator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases',
        limit_choices_to={'role': 'investigator'}
    )
    assigned_analyst = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analyst_cases'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CaseAnalysis(models.Model):
    RECOMMEND_CHOICES = [
        ('open', 'Keep Open'),
        ('investigating', 'Move to Review'),
        ('closed', 'Recommend Closure'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    analyst = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'analyst'}
    )
    evidence_summary = models.TextField()
    insights = models.TextField()
    patterns_identified = models.TextField(blank=True)
    recommended_status = models.CharField(max_length=20, choices=RECOMMEND_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.case.title}"

