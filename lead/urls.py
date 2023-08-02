from django.urls import path

from . import views

app_name = "lead"

urlpatterns = [
    path("", views.ListLeadView.as_view(), name="list"),
    path("add/", views.CreateLeadView.as_view(), name="create"),
    path("detail/<int:pk>/", views.LeadDetailView.as_view(), name="detail"),
]
