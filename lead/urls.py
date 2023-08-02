from django.urls import path

from . import views

app_name = "lead"

urlpatterns = [
    path("", views.LeadListView.as_view(), name="list"),
    path("add/", views.LeadCreateView.as_view(), name="create"),
    path("<int:pk>/detail/", views.LeadDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name="delete"),
    path("<int:pk>/update/", views.LeadUpdateView.as_view(), name="update"),
]
