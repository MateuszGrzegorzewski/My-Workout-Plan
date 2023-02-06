from rest_framework.serializers import ModelSerializer
from .models import TrainingMain, Training, TrainingName, PlanName, Plan

class TrainingMainSerializer(ModelSerializer):
    class Meta:
        model = TrainingMain
        fields = '__all__'
        exclude = ["user"]

class TrainingNameSerializer(ModelSerializer):
    class Meta:
        model = TrainingName
        fields = "__all__"
        exclude = ["user"]


class TrainingSerializer(ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"
        exclude = ["user", "name"]


class PlanNameSerializer(ModelSerializer):
    class Meta:
        model = PlanName
        fields = "__all__"
        exclude = ["user"]


class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
        exclude = ["user"]
