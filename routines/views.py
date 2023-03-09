from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import PlanModel, TrainingModel, TrainingExerciseModel, TrainingParametersModel
from .serializers import (PlanSerializer, TrainingExerciseSerializer,
                          TrainingParametersSerializer, TrainingSerializer)


class TrainingExercisePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TrainingPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class PlanPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10


class TrainingExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingExerciseSerializer
    pagination_class = TrainingExercisePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TrainingExerciseModel.objects.filter(user=user)
        return queryset


class TrainingViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingSerializer
    pagination_class = TrainingPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TrainingModel.objects.filter(user=user)
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
        queryset = TrainingParametersModel.objects.filter(user=user)
        return queryset

class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    pagination_class = PlanPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = PlanModel.objects.filter(user=user)
        return queryset
