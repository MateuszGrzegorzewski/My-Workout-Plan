from django.contrib import admin

from .models import TrainingName, TrainingMain, TrainingResult, PlanName, Plan

admin.site.register(TrainingName)
admin.site.register(TrainingMain)
admin.site.register(TrainingResult)
admin.site.register(PlanName)
admin.site.register(Plan)