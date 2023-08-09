from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response

from backend.models import Shop
from backend.serializers import ShopSerializer
from backend.views.base import CustomViewSet


@extend_schema_view(
    list=extend_schema(
        summary="Получить список Магазинов",
    ),
)
class ShopView(CustomViewSet):
    serializer_class = ShopSerializer

    def list(self, request, *args, **kwargs):
        queryset = Shop.objects.filter(state=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
