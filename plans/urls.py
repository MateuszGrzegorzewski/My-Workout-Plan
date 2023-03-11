from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("musclewiki/", include("musclewiki.urls")),
    path("plans/", include("routines.urls")),
]