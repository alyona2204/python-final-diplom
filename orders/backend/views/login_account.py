from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import serializers

from backend.views.base import CustomViewSet


class LoginAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class LoginAccount(CustomViewSet):
    serializer_class = LoginAccountSerializer

    def create(self, request, *args, **kwargs):
        # Проверяем наличие всех обязательных аргументов
        serializer = self.serializer_class(data=request.data)
        print(123)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.data['email'], password=serializer.data['password'])

            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)

                    return Response({'Status': True, 'Token': token.key})

            return Response({'Status': False, 'Errors': 'Не удалось авторизовать'})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
