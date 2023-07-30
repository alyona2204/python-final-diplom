from django.db.models import Q
from rest_framework.response import Response

from backend.models import ProductInfo
from backend.serializers import ProductInfoSerializer
from backend.views.base import CustomViewSet


class ProductInfoView(CustomViewSet):
    serializer_class = ProductInfoSerializer

    def list(self, request, *args, **kwargs):
        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')

        if shop_id:
            query = query & Q(shop_id=shop_id)

        if category_id:
            query = query & Q(product__category_id=category_id)

        queryset = ProductInfo.objects.filter(
            query).select_related('shop', 'product__category').prefetch_related('product_parameters__parameter').distinct()

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        query = Q(shop__state=True)

        queryset = ProductInfo.objects.filter(
            query).select_related('shop', 'product__category').prefetch_related('product_parameters__parameter').distinct()

        if pk:
            product_info_instance = queryset.filter(id=pk).first()
            if product_info_instance:
                serializer = self.serializer_class(product_info_instance)
                return Response(serializer.data)

        return Response({'Status': False, 'Error': 'Товар не найден'}, status=404)
