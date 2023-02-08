from django.urls import path, include
from rest_framework import routers

from .views import MuscleViewSet, ExerciseDetailUpdateDeleteAPIView, ExerciseCreateView


router = routers.DefaultRouter()
router.register(r'', MuscleViewSet, basename='muscles')

urlpatterns = [
    path('exercise/<int:pk>/', ExerciseDetailUpdateDeleteAPIView.as_view(),
         name='exercise-detail-update-delete'),
    path('exercise/', ExerciseCreateView.as_view(), name='exercise-create'),
]

urlpatterns += router.urls


# from . import views
# router.register(r'exercise/', ExerciseViewSet)
# router.register(r'<int:pk>/', ExerciseDetailAPIView, basename='exercise-detail')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# urlpatterns = [
#     path('', views.getMuscles),
#     path('<int:pk>', views.getExercises),

# ]

# NEXT URLS for views which I create
