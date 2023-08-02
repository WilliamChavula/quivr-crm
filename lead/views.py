from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, ListView, UpdateView, View

from .forms import LeadCreateForm
from .models import Lead


class LeadCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "lead/create.html"
    form_class = LeadCreateForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("lead:list")
    success_message = "Lead created successfully"

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        lead.save()

        return super(LeadCreateView, self).form_valid(form)


class LeadListView(LoginRequiredMixin, ListView):
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
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class LeadUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lead
    template_name = "lead/update.html"
    form_class = LeadCreateForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("lead:list")
    success_message = "Lead changes saved successfully"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class LeadDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk: int, *args, **kwargs):
        lead: Lead = get_object_or_404(Lead, pk=pk)

        lead.delete()

        messages.success(request, "Lead successfully deleted.")

        return redirect("lead:list")
