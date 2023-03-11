from django.contrib import admin

from .models import (Plan, Training, TrainingExercise, TrainingParameters,
                     TrainingResult)

admin.site.register(Training)
admin.site.register(TrainingExercise)
admin.site.register(TrainingParameters)
admin.site.register(Plan)
admin.site.register(TrainingResult)
