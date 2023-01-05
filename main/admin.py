from django.contrib import admin

from .models import TrainingName, TrainingMain, Training, Plan

admin.site.register(TrainingName)
admin.site.register(TrainingMain)
admin.site.register(Training)
admin.site.register(Plan)