from rest_framework import generics, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
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
    queryset = TrainingExerciseModel.objects.all()
    serializer_class = TrainingExerciseSerializer
    pagination_class = TrainingExercisePagination


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = TrainingModel.objects.all()
    serializer_class = TrainingSerializer
    pagination_class = TrainingPagination


class TrainingParametersViewSet(viewsets.ModelViewSet):
    queryset = TrainingParametersModel.objects.all()
    serializer_class = TrainingParametersSerializer
    pagination_class = TrainingPagination


class PlanViewSet(viewsets.ModelViewSet):
    queryset = PlanModel.objects.all()
    serializer_class = PlanSerializer
    pagination_class = PlanPagination
