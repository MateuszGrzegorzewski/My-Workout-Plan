import uuid

from django.conf import settings
from django.db import models


class Muscle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    @property
    def exercise_create_url(self):
        return "/musclewiki/exercise/"

    def __str__(self):
        return self.name


class Exercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    muscle = models.ManyToManyField(Muscle)
    technique = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update', 'created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name="unique_name_of_exercise")
        ]

    def __str__(self):
        return self.name
