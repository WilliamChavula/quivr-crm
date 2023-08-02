from typing import Final

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel


User: Final[UserModel] = get_user_model()


class Team(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_team"
    )
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, related_name="teams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
