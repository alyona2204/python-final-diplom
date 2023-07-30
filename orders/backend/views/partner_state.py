from distutils.util import strtobool
from rest_framework.response import Response
from rest_framework import serializers

from backend.views.base import CustomViewSet
from backend.models import Shop


class PartnerStateSerializer(serializers.Serializer):
    state = serializers.CharField(
        required=True,
        max_length=10,
        help_text="Состояние магазина ('on' или 'off')"
    )


class PartnerState(CustomViewSet):
    serializer_class = PartnerStateSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        try:
            shop = request.user.shop
            return Response({'state': 'on' if shop.state else 'off'}, status=200)
        except Shop.DoesNotExist as e:
            return Response({'Status': False, 'Error': 'Не создан магазин'}, status=403)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            state = serializer.data['state']
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
                shop = request.user.shop
                return Response({'state': 'on' if shop.state else 'off'}, status=200)
            except ValueError as error:
                return Response({'Status': False, 'Errors': str(error)})
            except Shop.DoesNotExist as e:
                return Response({'Status': False, 'Error': 'Не создан магазин'}, status=403)

        return Response({'error': serializer.errors})
