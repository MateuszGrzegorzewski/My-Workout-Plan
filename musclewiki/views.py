from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Exercise, Muscle
from .permissions import AuthorOrReadOnly, IsOwnerOrReadOnly
from .serializer import ExerciseSerializer, MuscleSerializer


class MuscleViewSet(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, pk=None):
        try:
            muscle = Muscle.objects.get(pk=pk)
        except:
            raise Http404

        if request.user.is_authenticated:
            exercises = Exercise.objects.filter(muscle__pk=pk).filter(
                user__is_staff=True) | Exercise.objects.filter(muscle__pk=pk).filter(user=request.user)
        else:
            exercises = Exercise.objects.filter(
                muscle__pk=pk).filter(user__is_staff=True)

        serializer = MuscleSerializer(muscle)
        serializer_exercise = ExerciseSerializer(
            exercises, many=True, context={'request': request})
        return Response({"muscle": serializer.data,
                        "exercise-create-route": "/musclewiki/exercise/create/",
                         "exercises": serializer_exercise.data})


class ExerciseDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except IntegrityError:
            return reverse('')

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ExerciseCreateView(generics.CreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return HttpResponseRedirect(redirect_to='/musclewiki/')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
