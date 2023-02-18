from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("musclewiki/", include("musclewiki.urls")),
]

handler404 = 'main.views.custom_page_not_found_view'