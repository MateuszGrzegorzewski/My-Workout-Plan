from django.contrib import admin

from .models import (PlanModel, TrainingExerciseModel, TrainingModel,
                     TrainingParametersModel, TrainingResultModel)

admin.site.register(TrainingModel)
admin.site.register(TrainingExerciseModel)
admin.site.register(TrainingParametersModel)
admin.site.register(PlanModel)
admin.site.register(TrainingResultModel)
