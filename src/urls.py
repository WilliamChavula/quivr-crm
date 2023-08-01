from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("userprofile.urls", namespace="accounts")),
    path("", include("core.urls", namespace="core")),
]
