from django.forms import ModelForm
from .models import TrainingMain, Training, TrainingName, PlanName, Plan


class TrainingMainForm(ModelForm):
    class Meta:
        model = TrainingMain
        fields = "__all__"
        exclude = ["user"]


class TrainingNameForm(ModelForm):
    class Meta:
        model = TrainingName
        fields = "__all__"
        exclude = ["user"]


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = "__all__"
        exclude = ["user", "name"]


class PlanNameForm(ModelForm):
    class Meta:
        model = PlanName
        fields = "__all__"
        exclude = ["user"]


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = "__all__"
        exclude = ["user"]
