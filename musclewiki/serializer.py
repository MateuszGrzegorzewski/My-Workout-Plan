from rest_framework import serializers

from .models import Exercise, Muscle


class MuscleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Muscle
        fields = '__all__'


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
