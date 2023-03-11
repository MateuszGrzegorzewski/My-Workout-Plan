from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueTogetherValidator

from .models import Exercise, Muscle


class MuscleSerializer(serializers.ModelSerializer):
    muscle_with_exercises_url = serializers.SerializerMethodField(
        read_only=True)
    exercise_create_url = serializers.ReadOnlyField()

    class Meta:
        model = Muscle
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Muscle.objects.all(), fields=['name'], message="This muscle already exist")]

    def get_muscle_with_exercises_url(self, obj):
        request = self.context.get('request')

        if request is None:
            return None
        return reverse("muscles-detail", kwargs={"pk": obj.pk}, request=request)


class ExerciseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='exercise-detail-update-delete')

    class Meta:
        model = Exercise
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Exercise.objects.all(), fields=['user', 'name'], message="This name of exercise already exist")]
