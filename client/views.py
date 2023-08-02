from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/list.html"
    context_object_name = "clients"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
