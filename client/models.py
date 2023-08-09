from typing import Final

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel
from django.contrib.contenttypes.fields import GenericRelation

from team.models import Team
from channel.models import Channel, Mode

User: Final[UserModel] = get_user_model()


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=12, verbose_name="Phone number", blank=True, null=True
    )
    social = models.URLField(blank=True, null=True, verbose_name="Social media link")
    address = models.TextField(verbose_name="Mailing address", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(Team, related_name="clients", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name="clients", on_delete=models.CASCADE
    )
    communication_channel = GenericRelation(Channel)
    preferred_communication = models.CharField(
        max_length=15, choices=Mode.choices, default=Mode.Email
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["email"], name="email_idx"),
        ]

    def __str__(self):
        return self.name
