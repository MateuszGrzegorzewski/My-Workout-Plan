from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Exercise, Muscle


class MuscleSerializer(serializers.ModelSerializer):
    muscle_with_exercises_url = serializers.HyperlinkedIdentityField(
        view_name='muscles-detail')
    exercise_create_url = serializers.ReadOnlyField()

    class Meta:
        model = Muscle
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Muscle.objects.all(), fields=['name'], message="This muscle already exist")]


class ExerciseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='exercise-detail-update-delete')

    class Meta:
        model = Exercise
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Exercise.objects.all(), fields=['user', 'name'], message="This name of exercise already exist")]
