from typing import Final

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel

from team.models import Team


User: Final[UserModel] = get_user_model()


class Role(models.TextChoices):
    Manager = "manager"
    Sales = "sales"
    Lead = "lead"
    Marketing = "marketing"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="userprofile", on_delete=models.CASCADE
    )
    role = models.CharField(max_length=12, choices=Role.choices, default=Role.Sales)
    team = models.ForeignKey(Team, related_name="employees", on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
