from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("auth/", include("userprofile.urls", namespace="accounts")),
    path("client/", include("client.urls", namespace="client")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("lead/", include("lead.urls", namespace="lead")),
    path("team/", include("team.urls", namespace="team")),
    path("", include("core.urls", namespace="core")),
]
