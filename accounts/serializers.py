from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name')


class CreateUserSerializer(serializers.ModelSerializer):
    is_staff = serializers.HiddenField(default=False)
    is_superuser = serializers.HiddenField(default=False)
    is_active = serializers.HiddenField(default=False)
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs
