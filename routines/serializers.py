from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueTogetherValidator

from .models import TrainingParametersModel, TrainingModel, PlanModel, TrainingExerciseModel


def current_user():
    return serializers.HiddenField(default=serializers.CurrentUserDefault())


class TrainingExerciseSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training_exercise-detail')

    # searching ???

    class Meta:
        model = TrainingExerciseModel
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=TrainingExerciseModel.objects.all(), fields=['user', 'name'], message="This name of exercise already exists")]


class TrainingSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='r_training-detail')

    class Meta:
        model = TrainingModel
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=TrainingModel.objects.all(), fields=['user', 'name'], message="This name of training already exists")]


class TrainingParametersSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training_parametres-detail')

    class Meta:
        model = TrainingParametersModel
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='r_plan-detail')

    class Meta:
        model = PlanModel
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=PlanModel.objects.all(), fields=['user', 'name'], message="This name of plan already exists")]
