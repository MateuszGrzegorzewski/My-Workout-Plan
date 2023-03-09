from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (PlanModel, TrainingExerciseModel, TrainingModel,
                     TrainingParametersModel)


def current_user():
    return serializers.HiddenField(default=serializers.CurrentUserDefault())


class TrainingExerciseSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training_exercise-detail')

    class Meta:
        model = TrainingExerciseModel
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=TrainingExerciseModel.objects.all(), fields=['user', 'name'], message="This name of exercise already exists")]


class TrainingParametersSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training_parameters-detail')
    exercise_name = serializers.ReadOnlyField(source='exercise.name')
    training_name = serializers.ReadOnlyField(source='name.name')

    class Meta:
        model = TrainingParametersModel
        fields = '__all__'

    def validate_name(self, value):
        user = self.context['request'].user
        ids = TrainingModel.objects.filter(user=user)
        if value not in ids:
            raise serializers.ValidationError("Error. Improper training")
        return value

    def validate_exercise(self, value):
        user = self.context['request'].user
        ids = TrainingExerciseModel.objects.filter(user=user)
        if value not in ids:
            raise serializers.ValidationError("Error. Improper exercise")
        return value


class TrainingSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='r_training-detail')
    parameters = serializers.SerializerMethodField()
    url_create_training_params = serializers.SerializerMethodField()

    class Meta:
        model = TrainingModel
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=TrainingModel.objects.all(), fields=['user', 'name'], message="This name of training already exists")]

    def get_parameters(self, obj):
        parameters = TrainingParametersModel.objects.filter(name__id=obj.id)
        serialized_parameters = TrainingParametersSerializer(
            parameters, many=True, context=self.context, read_only=True)
        return serialized_parameters.data

    def get_url_create_training_params(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri("/routines/training/param/")


class PlanSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='r_plan-detail')
    trainings_values = serializers.SerializerMethodField()

    class Meta:
        model = PlanModel
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=PlanModel.objects.all(), fields=['user', 'name'], message="This name of plan already exists")]

    def get_trainings_values(self, obj):
        training_objs = obj.training.all()
        training_serializer = TrainingSerializer(
            training_objs, many=True, context=self.context, read_only=True)
        return training_serializer.data

    def validate_training(self, value):
        user = self.context['request'].user
        ids = TrainingModel.objects.filter(user=user)
        if value not in ids:
            raise serializers.ValidationError(
                "Error. Improper training")
        return value
