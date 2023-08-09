from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from team.models import Team, Type


class Mode(models.TextChoices):
    Email = "email"
    Mail = "mail"
    Phone = "phone"
    Social = "social_media"


class Channel(models.Model):
    mode = models.CharField(max_length=15, choices=Mode.choices, db_index=True)
    team_contacting = models.ForeignKey(
        Team, on_delete=models.SET_DEFAULT, default=Type.Sales
    )
    date_contacted = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ["-date_contacted"]

    def __str__(self):
        return self.mode.capitalize()
