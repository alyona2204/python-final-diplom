from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework import serializers

from backend.serializers import UserSerializer
from backend.signals import new_user_registered
from backend.views.base import CustomViewSet
from backend.models import User


class RegisterAccount(CustomViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        required_fields = {'first_name', 'last_name', 'email', 'password', 'company', 'position'}

        # Проверяем наличие всех обязательных аргументов
        if required_fields.issubset(request.data):
            errors = {}

            # Проверяем пароль на сложность
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return Response({'Status': False, 'Errors': {'password': error_array}})
            else:
                # Проверяем данные для уникальности имени пользователя
                user_serializer = self.serializer_class(data=request.data)
                if user_serializer.is_valid():
                    # Сохраняем пользователя
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    new_user_registered.send(sender=self.__class__, user_id=user.id)
                    return Response({'Status': True})
                else:
                    return Response({'Status': False, 'Errors': user_serializer.errors})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
