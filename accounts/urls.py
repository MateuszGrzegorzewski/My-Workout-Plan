from django.urls import path
from knox.views import LogoutAllView, LogoutView

from . import views

urlpatterns = [
    path('register/', views.CreateUserAPI.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logoutall/', LogoutAllView.as_view(), name='logout-all'),
]
