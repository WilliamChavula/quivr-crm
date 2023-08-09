from django.urls import path

from . import views

app_name = "lead"

urlpatterns = [
    path("", views.LeadListView.as_view(), name="list"),
    path("add/", views.LeadCreateView.as_view(), name="create"),
    path("<int:pk>/make-client/", views.LeadToClientView.as_view(), name="make-client"),
    path("<int:pk>/detail/", views.LeadDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name="delete"),
    path("<int:pk>/update/", views.LeadUpdateView.as_view(), name="update"),
    path("confirm/<int:id>", views.ModalTemplateView.as_view(), name="modal"),
    path(
        "communication_channel_chart/",
        views.CommunicationChannelChartView.as_view(),
        name="communication_channel",
    ),
    path(
        "comm-by-yr/",
        views.CommunicationChannelByYearChartView.as_view(),
        name="comm-by-yr",
    ),
]
