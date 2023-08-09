from django.utils.html import format_html
import django_tables2 as tables

from client.models import Client
from lead.models import Lead


class LeadDashboardTable(tables.Table):
    class Meta:
        model = Lead
        orderable = True
        fields = ("name", "priority", "status")
        row_attrs = {"class": "border-b hover:bg-zinc-300 px-2"}


class ClientDashboardTable(tables.Table):
    class Meta:
        model = Client
        orderable = True
        fields = ("name", "team__name", "preferred_communication")
