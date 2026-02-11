import hashlib
from django.db import models
from django.conf import settings
from cases.models import Case
class Evidence(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='evidences'
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='case_uploaded_evidences'
    )

    file = models.FileField(upload_to='case_evidence/')
    description = models.TextField(blank=True)
    hash_code = models.CharField(
    max_length=64,
    unique=True,
    null=True,
    blank=True,
    editable=False
)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.hash_code and self.file:
            sha256 = hashlib.sha256()
            for chunk in self.file.chunks():
                sha256.update(chunk)
            self.hash_code = sha256.hexdigest()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.case.title} | {self.hash_code[:12]}"
