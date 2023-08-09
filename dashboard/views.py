from typing import Any, Dict

from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, View

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px

from client.models import Client
from lead.models import Lead


class DashboardView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        leads = Lead.objects.filter(created_by=request.user)[:5]
        clients = Client.objects.filter(created_by=request.user)[:5]

        context: Dict["str":Any] = {
            "leads": leads,
            "clients": clients,
        }
        return render(request, "dashboard/dashboard.html", context)


class DashboardLeadTableFilter(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        sort: str = request.GET.get("sort", "name")
        ascending: str = request.GET.get("asc", "true")

        if ascending == "true":
            ascending = "false"
        else:
            sort = f"-{sort}"
            ascending = "true"

        leads = Lead.objects.filter(created_by=request.user).order_by(sort)[:5]
        context = {"leads": leads, "asc": ascending}

        return render(request, "dashboard/partials/lead-tbl.html", context)


class DashboardClientTableFilter(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        sort: str = request.GET.get("arrange", "name")
        ascending: str = request.GET.get("asc", "true")

        if ascending == "true":
            ascending = "false"
        else:
            sort = f"-{sort}"
            ascending = "true"

        clients = Client.objects.filter(created_by=request.user)

        if sort == "team":
            clients = clients.order_by("team__name")[:5]
        else:
            clients = clients.order_by(sort)[:5]

        context = {"clients": clients, "asc": ascending}

        return render(request, "dashboard/partials/client-tbl.html", context)


class NumberOfLeadsPerTeamChartView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        grouped_leads = Lead.objects.values("teams__name").annotate(
            total_leads=Count("id"),
        )

        leads_chart = [
            {"Team": record["teams__name"], "Leads count": record["total_leads"]}
            for record in grouped_leads
        ]

        df = pd.DataFrame(leads_chart)
        color_discrete_map = {
            "Marketing": "rgb(191, 180, 143)",
            "Sales": "rgb(86, 78, 88)",
            "Support": "rgb(144, 78, 85)",
        }
        fig = px.bar(
            df,
            x="Team",
            y="Leads count",
            width=500,
            color="Team",
            title="Number of Leads per Team",
            color_discrete_map=color_discrete_map,
        )

        bar_plot = plot(fig, output_type="div")

        context = {"bar_plot": bar_plot}

        return render(request, "dashboard/partials/leads-chart.html", context)


class NumberOfClientsPerTeamChartView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        grouped_clients = Client.objects.values("team__name").annotate(
            total_clients=Count("id")
        )

        clients_chart = [
            {"Team": record["team__name"], "Clients count": record["total_clients"]}
            for record in grouped_clients
        ]

        df = pd.DataFrame(clients_chart)
        color_discrete_map = {
            "Marketing": "rgb(91, 133, 170)",
            "Sales": "rgb(65, 71, 112)",
            "Support": "rgb(55, 34, 72)",
        }

        fig = px.bar(
            df,
            x="Team",
            y="Clients count",
            width=500,
            color="Team",
            title="Number of Clients per Team",
            color_discrete_map=color_discrete_map,
        )

        bar_plot = plot(fig, output_type="div")

        context = {"bar_plot": bar_plot}

        return render(request, "dashboard/partials/clients-chart.html", context)


class LeadStatusGroupedView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/partials/lead_status_chart.html"

    def get_context_data(self, **kwargs):
        client_status = Lead.objects.values("status").annotate(status_count=Count("id"))

        context = super().get_context_data(**kwargs)
        status_chart = [
            {"Status": record["status"], "Status count": record["status_count"]}
            for record in client_status
        ]

        df = pd.DataFrame(status_chart)
        color_discrete_map = {
            "new": "rgb(112, 135, 127)",
            "won": "rgb(239, 148, 108)",
            "contacted": "rgb(196, 167, 125)",
            "lost": "rgb(47, 41, 99)",
        }

        fig = px.pie(
            df,
            values="Status count",
            names="Status",
            color="Status",
            color_discrete_map=color_discrete_map,
            title="Lead Count by Status",
        )
        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

        bar_plot = plot(fig, output_type="div")

        context["bar_plot"] = bar_plot

        return context


class IsClientGroupedView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/partials/is_client_chart.html"

    def get_context_data(self, **kwargs):
        is_client_grouped = Lead.objects.values("is_client").annotate(
            is_client_count=Count("id")
        )

        context = super().get_context_data(**kwargs)
        is_client_chart = [
            {
                "Is Client": record["is_client"],
                "Is Client count": record["is_client_count"],
            }
            for record in is_client_grouped
        ]

        df = pd.DataFrame(is_client_chart)

        color_discrete_map = {
            False: "rgb(11, 60, 73)",
            True: "rgb(6, 141, 157)",
        }

        fig = px.bar(
            df,
            y="Is Client count",
            x="Is Client",
            color="Is Client",
            color_discrete_map=color_discrete_map,
            title="Count of leads who became clients",
            width=450,
            category_orders={"Is Client": [False, True]},
        )

        bar_plot = plot(fig, output_type="div")

        context["bar_plot"] = bar_plot

        return context
