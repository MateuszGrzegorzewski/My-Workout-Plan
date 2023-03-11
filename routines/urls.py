from django.urls import include, path
from rest_framework import routers

from .views import (PlanViewSet, TrainingExerciseViewSet,
                    TrainingParametersViewSet, TrainingResultViewSet,
                    TrainingViewSet)

router = routers.DefaultRouter()
router.register(r'training/exercise', TrainingExerciseViewSet,
                basename="training_exercise")
router.register(r'training/param', TrainingParametersViewSet,
                basename="training_parameters")
router.register(r'training/result', TrainingResultViewSet,
                basename="training_result")
router.register(r'training', TrainingViewSet, basename="training")
router.register(r'', PlanViewSet, basename="plan")


urlpatterns = [
    path("", include(router.urls)),
]
