from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="board"),
    path("sort-leads/", views.DashboardLeadTableFilter.as_view(), name="sort-leads"),
    path(
        "sort-clients/", views.DashboardClientTableFilter.as_view(), name="sort-client"
    ),
    path(
        "leads-chart/",
        views.NumberOfLeadsPerTeamChartView.as_view(),
        name="leads-chart",
    ),
    path(
        "clients-chart/",
        views.NumberOfClientsPerTeamChartView.as_view(),
        name="clients-chart",
    ),
    path(
        "lead_status_chart/",
        views.LeadStatusGroupedView.as_view(),
        name="lead_status_chart",
    ),
    path(
        "is_client_chart/", views.IsClientGroupedView.as_view(), name="is_client_chart"
    ),
]
