from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, DetailView

from .forms import LeadCreateForm
from .models import Lead


class CreateLeadView(LoginRequiredMixin, FormView):
    template_name = "lead/create.html"
    form_class = LeadCreateForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("dashboard:board")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        lead.save()

        return super(CreateLeadView, self).form_valid(form)


class ListLeadView(LoginRequiredMixin, ListView):
    model = Lead
    context_object_name = "leads"
    template_name = "lead/list.html"

    def get_queryset(self):
        # original qs
        qs = super().get_queryset()
        # filter by a variable captured from url, for example
        return qs.filter(created_by=self.request.user)


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    context_object_name = "lead"
    template_name = "lead/detail.html"

    def get_queryset(self):
        # original qs
        qs = super().get_queryset()
        # filter by a variable captured from url, for example
        return qs.filter(created_by=self.request.user)
