from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path("", views.home, name='home'),
    path("plan/", views.plan, name='plan'),
    path("training/", views.training, name='training'),
    path("training/<str:pk>/", views.training_pk, name='training'),

    path("create-training/", views.createTraining,
         name="create-training"),
    path("update-training/<str:pk>/", views.updateTraining,
         name="update-training"),
    path("delete-training/<str:pk>/", views.deleteTraining,
         name="delete-training"),
     path("create-exercise/", views.createExercise,
         name="create-exercise"),
     path("update-exercise/<str:pk>/", views.updateExercise,
         name="update-exercise"),
    path("delete-exercise/<str:pk>/", views.deleteExercise,
         name="delete-exercise"),
     path("create-exercise-scores/", views.createExerciseScores,
         name="create-exercise-score"),
     path("update-exercise-scores/<str:pk>/", views.updateExerciseScores,
         name="update-exercise-score"),
    path("delete-exercise-scores/<str:pk>/", views.deleteExerciseScores,
         name="delete-exercise-score"),
]
