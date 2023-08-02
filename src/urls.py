from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("userprofile.urls", namespace="accounts")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("lead/", include("lead.urls", namespace="lead")),
    path("", include("core.urls", namespace="core")),
]
