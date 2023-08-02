from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, FormView, ListView, UpdateView, View

from .forms import ClientCreationForm
from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/list.html"
    context_object_name = "clients"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    context_object_name = "client"
    template_name = "client/detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class ClientCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ClientCreationForm
    template_name = "client/create.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("client:list")
    success_message = "Client created successfully"

    def form_valid(self, form):
        client = form.save(commit=False)
        client.created_by = self.request.user
        client.save()

        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    template_name = "client/update.html"
    form_class = ClientCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("client:list")
    success_message = "Client details changed."

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class ClientDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk: int, *args, **kwargs):
        client: Client = get_object_or_404(Client, pk=pk)

        client.delete()

        messages.info(request, "Client deleted.")

        return redirect("client:list")
