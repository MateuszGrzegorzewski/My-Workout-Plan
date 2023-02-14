from django.db import models
from django.contrib.auth.models import User


class TrainingName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_name_of_training")
        ]

    def __str__(self):
        return self.name


class TrainingMain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(TrainingName, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=100)
    series = models.IntegerField(null=True, blank=True)
    reps = models.CharField(max_length=10, null=True, blank=True)
    tempo = models.CharField(max_length=10, null=True, blank=True)
    rir = models.CharField(max_length=10, null=True, blank=True)
    rest = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name', 'exercise'], name="unique_exercise_of_training")
        ]

    def __str__(self):
        return self.exercise


class TrainingResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(TrainingName, on_delete=models.CASCADE)
    exercise = models.ForeignKey(TrainingMain, on_delete=models.CASCADE)
    series = models.CharField(max_length=15, default="Serie nr: ")
    weight = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    rir = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.series


class PlanName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_name_of_plan")
        ]

    def __str__(self):
        return self.name


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(PlanName, on_delete=models.CASCADE)
    training = models.ForeignKey(TrainingName, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name', 'training'], name="unique_training_of_plan")
        ]
