from django.contrib.auth import login
from knox import views as knox_views
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CreateUserSerializer, LoginSerializer


class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)

            response = super().post(request, format=None)

        return Response(response.data, status=status.HTTP_200_OK)
