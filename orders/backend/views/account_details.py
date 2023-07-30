from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework import serializers

from backend.views.base import CustomViewSet
from backend.models import User


class UserSerializer(serializers.ModelSerializer):
    # Определите сериализатор для пользователя

    class Meta:
        model = User
        fields = '__all__'


class AccountDetails(CustomViewSet):
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        # Проверяем пароль на сложность
        if 'password' in request.data:
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return Response({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.user.set_password(request.data['password'])

        # Проверяем остальные данные
        user_serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'Status': True})
        else:
            return Response({'Status': False, 'Errors': user_serializer.errors})
