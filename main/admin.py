from django.contrib import admin

from .models import TrainingName, TrainingMain, Training, PlanName, Plan

admin.site.register(TrainingName)
admin.site.register(TrainingMain)
admin.site.register(Training)
admin.site.register(PlanName)
admin.site.register(Plan)