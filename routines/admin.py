from django.contrib import admin

from .models import TrainingParametersModel, TrainingModel, PlanModel, TrainingExerciseModel

admin.site.register(TrainingModel)
admin.site.register(TrainingExerciseModel)
admin.site.register(TrainingParametersModel)
admin.site.register(PlanModel)
