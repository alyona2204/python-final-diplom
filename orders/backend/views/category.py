from rest_framework.response import Response

from backend.models import Category
from backend.serializers import CategorySerializer
from backend.views.base import CustomViewSet


class CategoryView(CustomViewSet):
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
