from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly, AuthorOrReadOnly
from .serializer import MuscleSerializer, ExerciseSerializer
from .models import Exercise, Muscle


class MuscleViewSet(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, pk=None):
        queryset = Muscle.objects.all()
        muscle = get_object_or_404(queryset, pk=pk)

        if request.user.is_authenticated:
            exercises = Exercise.objects.filter(muscle__pk=pk).filter(
                user__is_staff=True) | Exercise.objects.filter(muscle__pk=pk).filter(user=request.user)
        else:
            exercises = Exercise.objects.filter(
                muscle__pk=pk).filter(user__is_staff=True)

        serializer = MuscleSerializer(muscle)
        serializer_exercise = ExerciseSerializer(exercises, many=True)
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


# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework import mixins

# class MusclesViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Muscle.objects.all()
#         serializer = MuscleSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Muscle.objects.all()
#         muscle = get_object_or_404(queryset, pk=pk)
#         exercises = Exercise.objects.filter(muscle__pk=pk)
#         serializer = MuscleSerializer(muscle)
#         serializer_exercise = ExerciseSerializer(exercises, many=True)
#         return Response({"muscle": serializer.data,
#                          "exercises": serializer_exercise.data})

#     def create(self, request):
#         serializer = MuscleSerializer(data=request.data)
#         permission_classes = [IsAdminUser]

#         if serializer.is_valid():
#             Muscle.objects.create(**serializer.validated_data)
#             return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

#         return Response({'status': 'Bad Request',
#                          'message': serializer.is_valid()},
#                           status=status.HTTP_400_BAD_REQUEST)

# class ExerciseViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Exercise.objects.all()
#         serializer = ExerciseSerializer(queryset, many=True)
#         return Response(serializer.data)

# @api_view(["GET", "POST"])
# def getMuscles(request):
#     muscles = Muscle.objects.all()
#     serializer = MuscleSerializer(
#         muscles, many=True, context={'request': request})

#     if request.method == 'POST':
#         muscle = MuscleSerializer(data = request.data)
#         if Muscle.objects.filter(**request.data).exists():
#             raise serializer.ValidationError('This data already exists')

#         if muscle.is_valid():
#             muscle.save()
#             return Response(muscle.data)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     return Response(serializer.data)


# @api_view(["GET"])
# def getExercises(request, pk):
#     exercise = Exercise.objects.filter(muscle__pk=pk)
#     serializer = ExerciseSerializer(
#         exercise, many=True, context={'request': request})
#     return Response(serializer.data)

# Next: POST PUT DELETE muscles - only admin
# POST PUT DELETE exercise
# Everyone see  (GET) only muscles and exercises which admin added

#  CREATE html file and display it on this file and others things
