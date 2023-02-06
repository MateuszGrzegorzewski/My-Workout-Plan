from django.db import models
from django.contrib.auth.models import User


class Muscle(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Muslces to add to DB
# muscles = ['forearms', 'biceps', 'triceps', 'shoulders', 'chest',
#            'ABS', 'back', 'glutes', 'quads', 'hamstrings', 'adductors', 'calves']


class Exercise(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    muscle = models.ForeignKey(
        Muscle, on_delete=models.CASCADE)
    technique = models.TextField()

    def __str__(self):
        return self.name
