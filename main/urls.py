from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("plan/", views.plan, name='plan'),
    path("training/", views.trainings, name='training'),
    path("training/<str:pk>/", views.training, name='training'),

    path("create-training/", views.createTraining,
         name="create-training"),
    path("update-training/<str:pk>/", views.updateTraining,
         name="update-training"),
    path("delete-training/<str:pk>/", views.deleteTraining,
         name="delete-training"),

    path("update-exercise/<str:pk>/", views.updateExercise,
         name="update-exercise"),
    path("delete-exercise/<str:pk>/", views.deleteExercise,
         name="delete-exercise"),

    path("create-exercise-scores/<str:pk_training>/", views.createExerciseScores,
         name="create-exercise-score"),
    path("update-exercise-scores/<str:pk>/", views.updateExerciseScores,
         name="update-exercise-score"),
    path("delete-exercise-scores/<str:pk>/", views.deleteExerciseScores,
         name="delete-exercise-score"),

    path("create-plan/", views.createPlan, name="create-plan"),
    path("update-plan/<str:pk>/", views.updatePlan, name="update-plan"),
    path("delete-plan/<str:pk>/", views.deletePlan, name="delete-plan"),

    path("add-training-to-plan/", views.addTrainingToPlan,
         name="add-training-to-plan"),
    path("delete-training-from-plan/<str:pk>/",
         views.deleteTrainingFromPlan, name="delete-training-from-plan"),
]
