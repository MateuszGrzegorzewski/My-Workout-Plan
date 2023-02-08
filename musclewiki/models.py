from django.db import models
from django.contrib.auth.models import User


class Muscle(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

# Muscles to add to DB
# muscles = ['forearms', 'biceps', 'triceps', 'shoulders', 'chest',
#            'ABS', 'back', 'glutes', 'quads', 'hamstrings', 'adductors', 'calves']


class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    muscle = models.ManyToManyField(Muscle)
    technique = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_name_of_exercise")
        ]

    def __str__(self):
        return self.name
