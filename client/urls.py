from django.urls import path
from . import views

app_name = "client"

urlpatterns = [
    path("", views.ClientListView.as_view(), name="list"),
    path("<int:pk>/detail/", views.ClientDetailView.as_view(), name="detail"),
]
