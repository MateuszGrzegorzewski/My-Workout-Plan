from django.db import models
from django.contrib.auth.models import User


class TrainingExerciseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_exercise_of_training_name")
        ]

    def __str__(self):
        return self.name


class TrainingModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_training_name")
        ]

    def __str__(self):
        return self.name


class TrainingParametersModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    exercise = models.ForeignKey(TrainingExerciseModel, on_delete=models.CASCADE)
    series = models.IntegerField(null=True, blank=True)
    reps = models.CharField(max_length=10, null=True, blank=True)
    tempo = models.CharField(max_length=10, null=True, blank=True)
    rir = models.CharField(max_length=10, null=True, blank=True)
    rest = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name.name}-{self.exercise.name}'


class PlanModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    training = models.ManyToManyField(TrainingModel)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_plan_name")
        ]

    def __str__(self):
        return self.name

#  adding training results and next things
