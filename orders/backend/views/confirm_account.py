from rest_framework.response import Response
from rest_framework import serializers

from backend.views.base import CustomViewSet
from backend.models import ConfirmEmailToken


class ConfirmEmailTokenSerializer(serializers.ModelSerializer):
    # Определите сериализатор для подтверждения почтового адреса

    class Meta:
        model = ConfirmEmailToken
        fields = '__all__'


class ConfirmAccount(CustomViewSet):
    serializer_class = ConfirmEmailTokenSerializer

    def create(self, request, *args, **kwargs):
        required_fields = {'email', 'token'}

        # Проверяем наличие всех обязательных аргументов
        if required_fields.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return Response({'Status': True})
            else:
                return Response({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
