import datetime
import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TrainingExercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update', 'created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_exercise_of_training_name")
        ]

    def __str__(self):
        return self.name


class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update', 'created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_training_name")
        ]

    def __str__(self):
        return self.name


class TrainingParameters(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.ForeignKey(Training, on_delete=models.CASCADE)
    exercise = models.ForeignKey(
        TrainingExercise, on_delete=models.CASCADE)
    series = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)])
    reps = models.CharField(max_length=10, null=True, blank=True)
    tempo = models.CharField(max_length=5, null=True, blank=True)
    rir = models.CharField(max_length=4, null=True, blank=True)
    rest = models.FloatField(validators=[MinValueValidator(
        0), MaxValueValidator(30)], null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update', 'created']

    def __str__(self):
        return f'{self.name.name}-{self.exercise.name}'


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    training = models.ManyToManyField(Training)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update', 'created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_plan_name")
        ]

    def __str__(self):
        return self.name


class TrainingResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    training = models.ForeignKey(
        TrainingParameters, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    serie_nr = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)])
    weight = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)])
    reps = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)])
    rir = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10)], null=True, blank=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'training', 'date', 'serie_nr'], name="unique_serie_for_todays_training")
        ]

    def __str__(self):
        return f'{self.training.name}-{self.training.exercise}-{self.serie_nr}'
