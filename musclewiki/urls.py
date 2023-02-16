from django.urls import include, path
from rest_framework import routers

from .views import (ExerciseCreateView, ExerciseDetailUpdateDeleteAPIView,
                    MuscleViewSet)

router = routers.DefaultRouter()
router.register(r'', MuscleViewSet, basename='muscles')

urlpatterns = [
    path("", include((router.urls, 'musclewiki'))),
    path('exercise/<int:pk>/', ExerciseDetailUpdateDeleteAPIView.as_view(),
         name='exercise-detail-update-delete'),
    path('exercise/create/', ExerciseCreateView.as_view(), name='exercise-create'),
]
