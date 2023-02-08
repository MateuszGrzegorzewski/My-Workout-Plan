from rest_framework import serializers

from .models import Exercise, Muscle


class MuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muscle
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Exercise
        fields = '__all__'
