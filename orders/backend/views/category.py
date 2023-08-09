from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response

from backend.models import Category
from backend.serializers import CategorySerializer
from backend.views.base import CustomViewSet


@extend_schema_view(
    list=extend_schema(
        summary="Получить список Категорий",
    ),
)
class CategoryView(CustomViewSet):
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
