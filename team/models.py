from typing import Final

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel


User: Final[UserModel] = get_user_model()


class Type(models.TextChoices):
    Marketing = "marketing"
    Sales = "sales"
    Support = "support"


class Team(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_team"
    )
    name = models.CharField(max_length=128, verbose_name="Team name")
    department = models.CharField(
        max_length=12, choices=Type.choices, default=Type.choices
    )
    members = models.ManyToManyField(User, related_name="teams")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["name"], name="name_idx")]

    def __str__(self):
        return self.name
