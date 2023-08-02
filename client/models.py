from typing import Final

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel

User: Final[UserModel] = get_user_model()


class Client(models.Model):
    name = models.CharField(max_length=255, help_text="Name of Client")
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name="clients", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}"