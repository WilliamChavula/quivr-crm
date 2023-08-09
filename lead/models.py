from typing import Final

from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel
from django.contrib.contenttypes.fields import GenericRelation

from team.models import Team
from channel.models import Channel, Mode

User: Final[UserModel] = get_user_model()


class Priority(models.TextChoices):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LeadStatus(models.TextChoices):
    NEW = "new"
    CONTACTED = "contacted"
    WON = "won"
    LOST = "lost"


class Lead(models.Model):
    name = models.CharField(max_length=255, help_text="Name or Company of the lead")
    teams = models.ForeignKey(Team, related_name="leads", on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=12, verbose_name="Phone number", blank=True, null=True
    )
    social = models.URLField(blank=True, null=True, verbose_name="Social media link")
    address = models.TextField(verbose_name="Mailing address", blank=True, null=True)
    communication_channel = GenericRelation(Channel)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="leads", on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=8, choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=10, choices=LeadStatus.choices, default=LeadStatus.NEW
    )

    preferred_communication = models.CharField(
        max_length=15,
        choices=Mode.choices,
    )
    is_client = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"], name="status_idx"),
            models.Index(fields=["priority"], name="priority_idx"),
            models.Index(fields=["is_client"], name="is_client_idx"),
        ]

    def __str__(self):
        return self.name


@receiver(post_save, sender="lead.Lead")
def create_client_when_lead_is_client(sender, instance: Lead, **kwargs):
    if instance.is_client and instance.status == LeadStatus.WON:
        from client.models import Client

        # check if no instance of client exists
        client = Client.objects.filter(email=instance.email)

        if client.exists():
            # do nothing if instance of client already exists
            # this can happen if client was created before creating Lead
            return
        # create client if it doesn't exist
        Client.objects.create(
            name=instance.name,
            email=instance.email,
            phone=instance.phone,
            social=instance.social,
            address=instance.address,
            description=instance.description,
            created_by=instance.created_by,
            preferred_communication=instance.preferred_communication,
            team=instance.teams,
        )


# Todo:
#   - Add channel Model which will capture information about:
#       1. when the communication took place
#       2. Lead or Client that was communicated with
#       3. notes describing the communication, decisions or resolutions, if any.
#   - set automatic reminders for each contact to sale team
#   - Introduce timeframe for contacting new Leads? Especially HIGH priority.
