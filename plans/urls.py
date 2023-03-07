from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("musclewiki/", include("musclewiki.urls")),
    path("", include("main.urls")),
]

handler404 = 'main.views.custom_page_not_found_view'