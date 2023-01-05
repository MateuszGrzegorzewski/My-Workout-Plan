from django.forms import ModelForm
from .models import TrainingMain, Training, TrainingName


class TrainingMainForm(ModelForm):
    class Meta:
        model = TrainingMain
        fields = "__all__"


class TrainingNameForm(ModelForm):
    class Meta:
        model = TrainingName
        fields = "__all__"


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = "__all__"
