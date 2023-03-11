from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import (Plan, Training, TrainingExercise, TrainingParameters,
                     TrainingResult)
from .serializers import (PlanSerializer, TrainingExerciseSerializer,
                          TrainingParametersSerializer,
                          TrainingResultSerializer, TrainingSerializer)


class TrainingExercisePagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class TrainingPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 50


class PlanPagination(PageNumberPagination):
    page_size = 1
    max_page_size = 10


class TrainingExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingExerciseSerializer
    pagination_class = TrainingExercisePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TrainingExercise.objects.filter(user=user)
        return queryset


class TrainingViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingSerializer
    pagination_class = TrainingPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Training.objects.filter(user=user)
        return queryset


class TrainingParametersViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = TrainingParametersSerializer
    pagination_class = TrainingPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TrainingParameters.objects.filter(user=user)
        return queryset


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    pagination_class = PlanPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Plan.objects.filter(user=user)
        return queryset


class TrainingResultViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingResultSerializer
    pagination_class = TrainingPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TrainingResult.objects.filter(user=user)
        return queryset
