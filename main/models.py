from django.db import models
from django.contrib.auth.models import User


class TrainingName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TrainingMain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(TrainingName, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=100, default="")
    series = models.IntegerField(null=True, blank=True)
    reps = models.CharField(max_length=10, blank=True)
    tempo = models.CharField(max_length=10, blank=True)
    rir = models.CharField(max_length=10, blank=True)
    rest = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.exercise


class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.ForeignKey(TrainingName, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(PlanName, on_delete=models.CASCADE)
    training = models.ForeignKey(TrainingName, on_delete=models.CASCADE)
    

