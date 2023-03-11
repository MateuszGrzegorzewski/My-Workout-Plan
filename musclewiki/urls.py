from django.urls import include, path
from rest_framework import routers

from .views import (ExerciseCreateView, ExerciseDetailUpdateDeleteAPIView,
                    MuscleViewSet)

router = routers.DefaultRouter()
router.register(r'', MuscleViewSet, basename='muscles')

urlpatterns = [
    path('exercise/', ExerciseCreateView.as_view(), name='exercise-create'),
    path('exercise/<str:pk>/', ExerciseDetailUpdateDeleteAPIView.as_view(),
         name='exercise-detail-update-delete'),
    path("", include(router.urls)),  
]
