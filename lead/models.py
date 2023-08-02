from typing import Final

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel

from team.models import Team

User: Final[UserModel] = get_user_model()


class Lead(models.Model):
    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    class LeadStatus(models.TextChoices):
        NEW = "new"
        CONTACTED = "contacted"
        WON = "won"
        LOST = "lost"

    name = models.CharField(max_length=255, help_text="Name or Company of the lead")
    teams = models.ForeignKey(Team, related_name="leads", on_delete=models.CASCADE)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="leads", on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=8, choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=10, choices=LeadStatus.choices, default=LeadStatus.NEW
    )
    is_client = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}"
