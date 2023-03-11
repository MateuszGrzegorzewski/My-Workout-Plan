import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (Plan, Training, TrainingExercise, TrainingParameters,
                     TrainingResult)


def current_user():
    return serializers.HiddenField(default=serializers.CurrentUserDefault())


class TrainingExerciseSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training_exercise-detail')

    class Meta:
        model = TrainingExercise
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=TrainingExercise.objects.all(), fields=['user', 'name'], message="This name of exercise already exists")]


class TrainingParametersSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training_parameters-detail')
    exercise_name = serializers.ReadOnlyField(source='exercise.name')
    training_name = serializers.ReadOnlyField(source='name.name')

    class Meta:
        model = TrainingParameters
        fields = '__all__'

    def validate_name(self, value):
        user = self.context['request'].user
        ids = Training.objects.filter(user=user)
        if value not in ids:
            raise serializers.ValidationError("Error. Improper training")
        return value

    def validate_exercise(self, value):
        user = self.context['request'].user
        ids = TrainingExercise.objects.filter(user=user)
        if value not in ids:
            raise serializers.ValidationError("Error. Improper exercise")
        return value

    def validate_reps(self, value):
        if value and not value.isdigit() and not re.match(r'^[1-9999]+-[1-9999]+$', value):
            raise serializers.ValidationError(
                'Reps must be a number or number-number (e.g. 5 or 5-8).')
        return value

    def validate_tempo(self, value):
        if value and not re.match(r'^[0-9,X][0-9,X][0-9,X][0-9,X]+$', value):
            raise serializers.ValidationError(
                'The tempo must be written in this way, e.g. 2011 oraz 31X1')
        return value

    def validate_rir(self, value):
        if value and not value.isdigit() and not re.match(r'^([0-9]|10)-([0-9]|10)$', value):
            raise serializers.ValidationError(
                'RIR must be a number or number-number (e.g. 1 or 1-2).')
        return value

    def validate_rest(self, value):
        if value and value % 0.5 != 0:
            raise serializers.ValidationError(
                'Rest must be a number or a decimal number ending with .5 (e.g. 1.5 or 3)')
        return value


class TrainingSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training-detail')
    parameters = serializers.SerializerMethodField()
    url_create_training_params = serializers.SerializerMethodField()

    class Meta:
        model = Training
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Training.objects.all(), fields=['user', 'name'], message="This name of training already exists")]

    def get_parameters(self, obj):
        parameters = TrainingParameters.objects.filter(name__id=obj.id)
        serialized_parameters = TrainingParametersSerializer(
            parameters, many=True, context=self.context, read_only=True)
        return serialized_parameters.data

    def get_url_create_training_params(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri("/routines/training/param/")


class PlanSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='plan-detail')
    trainings_values = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Plan.objects.all(), fields=['user', 'name'], message="This name of plan already exists")]

    def get_trainings_values(self, obj):
        training_objs = obj.training.all()
        training_serializer = TrainingSerializer(
            training_objs, many=True, context=self.context, read_only=True)
        return training_serializer.data

    def validate_training(self, value):
        user = self.context['request'].user
        valid_training_ids = user.training_set.values_list(
            'id', flat=True)
        invalid_training_ids = [
            t.id for t in value if t.id not in valid_training_ids]
        if invalid_training_ids:
            raise serializers.ValidationError("Error. Improper training")
        return value


class TrainingResultSerializer(serializers.ModelSerializer):
    user = current_user()
    url_detail = serializers.HyperlinkedIdentityField(
        view_name='training_result-detail')
    exercise_name = serializers.ReadOnlyField(source='training.name.name')
    training_name = serializers.ReadOnlyField(source='training.exercise.name')
    training_series = serializers.ReadOnlyField(source='training.series')

    class Meta:
        model = TrainingResult
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=TrainingResult.objects.all(), fields=['user', 'training', 'date', 'serie_nr'], message="It is impossible to set the same serie for today's training")]

    def validate_serie_nr(self, value):
        training = self.initial_data.get('training')

        if value > TrainingParameters.objects.get(id=training).series:
            raise serializers.ValidationError(
                "Error. Saved training has fewer series")
        return value
