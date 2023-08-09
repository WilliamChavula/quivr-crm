from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View,
    TemplateView,
)
from django.db.models import Count

from plotly.offline import plot
import plotly.express as px
import pandas as pd

from .forms import LeadCreateForm
from .models import Lead, LeadStatus

from core.views import ModalMixin
from channel.models import Channel
from team.models import Team


class LeadCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "lead/create.html"
    form_class = LeadCreateForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("lead:list")
    success_message = "Lead created successfully"

    def form_valid(self, form):
        lead = form.save(commit=False)

        team = Team.objects.get(name__iexact="sales")
        lead.created_by = self.request.user
        lead.teams = team
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
        return qs.filter(created_by=self.request.user, is_client=False)


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
    def get(self, request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponse:
        lead: Lead = get_object_or_404(Lead, pk=pk)

        lead.delete()

        response = HttpResponse()
        response["HX-Redirect"] = reverse_lazy("lead:list")

        messages.info(request, "Lead deleted.")

        return response


class LeadToClientView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponse:
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

        lead.is_client = True
        lead.status = LeadStatus.WON
        lead.save()

        messages.success(request, f"Congratulations! Lead {lead.name} is now a client")

        return redirect("lead:list")


class ModalTemplateView(ModalMixin, TemplateView):
    template_name = "lead/partials/modal.html"


class CommunicationChannelChartView(LoginRequiredMixin, TemplateView):
    template_name = "lead/partials/communication_channel_chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lead_id = self.request.GET.get("lead_id")

        if lead_id is None:
            context["plt_div"] = "No data yet for this lead. Please check later."
            return context

        lead = Lead.objects.get(pk=lead_id)

        channel_communication_count = (
            Channel.objects.filter(object_id=lead_id)
            .values("mode")
            .annotate(comm_count=Count("mode"))
            .filter(content_type__app_label="lead")
        )

        channel_communication_data = [
            {
                "communication mode": record["mode"],
                "count": record["comm_count"],
            }
            for record in channel_communication_count
        ]

        color_discrete_map = {
            "email": "rgb(7, 0, 77)",
            "mail": "rgb(45, 130, 183)",
            "social_media": "rgb(66, 226, 184)",
            "phone": "rgb(235, 138, 144)",
        }
        channel_communication_df = pd.DataFrame(channel_communication_data)
        bar_plot = px.bar(
            channel_communication_df,
            x="communication mode",
            y="count",
            color="communication mode",
            color_discrete_map=color_discrete_map,
            title="Communication Mode Count",
            width=800,
        )

        plt_div = plot(bar_plot, output_type="div", config={"displaylogo": False})

        context["plt_div"] = plt_div

        return context


class CommunicationChannelByYearChartView(LoginRequiredMixin, TemplateView):
    template_name = "lead/partials/communication_channel_by_yr_chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lead_id = self.request.GET.get("lead_id")

        if lead_id is None:
            context["plt_div"] = "No data yet for this lead. Please check later."
            return context

        channel_communication_count = (
            Channel.objects.filter(object_id=lead_id)
            .values("mode", "date_contacted__year")
            .annotate(comm_yr=Count("mode"))
            .filter(content_type__app_label="lead")
        )

        channel_communication_data = [
            {
                "communication mode": record["mode"],
                "year contacted": record["date_contacted__year"],
                "count": record["comm_yr"],
            }
            for record in channel_communication_count
        ]

        color_discrete_map = {
            "email": "rgb(7, 0, 77)",
            "mail": "rgb(45, 130, 183)",
            "social_media": "rgb(66, 226, 184)",
            "phone": "rgb(235, 138, 144)",
        }
        channel_communication_df = pd.DataFrame(channel_communication_data)
        bar_plot = px.bar(
            channel_communication_df,
            x="year contacted",
            y="count",
            barmode="group",
            color="communication mode",
            color_discrete_map=color_discrete_map,
            title="Communication Mode Count By Year",
            width=800,
        )

        plt_div = plot(bar_plot, output_type="div", config={"displaylogo": False})

        context["plt_div"] = plt_div

        return context
