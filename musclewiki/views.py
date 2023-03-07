from rest_framework import generics, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Exercise, Muscle
from .permissions import AuthorOrReadOnly, IsOwnerOrReadOnly
from .serializer import ExerciseSerializer, MuscleSerializer


class MuscleViewSet(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, pk=None):
        instance = self.get_object()

        if request.user.is_authenticated:
            exercises = Exercise.objects.filter(muscle__pk=pk).filter(
                user__is_staff=True) | Exercise.objects.filter(muscle__pk=pk).filter(user=request.user)
        else:
            exercises = Exercise.objects.filter(
                muscle__pk=pk).filter(user__is_staff=True)

        serializer = MuscleSerializer(instance)
        serializer_exercise = ExerciseSerializer(
            exercises, many=True, context={'request': request})
        return Response({"muscle": serializer.data,
                         "exercises": serializer_exercise.data})


class ExerciseDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrReadOnly]


class ExerciseCreateView(generics.CreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
