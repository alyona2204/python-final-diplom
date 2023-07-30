from django.db.models import Q, Sum, F
from django.db.utils import IntegrityError
from rest_framework.response import Response

from backend.models import Order, OrderItem
from backend.serializers import BasketSerializer, OrderItemSerializer
from backend.views.base import CustomViewSet


class BasketView(CustomViewSet):
    serializer_class = BasketSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = self.serializer_class(basket, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = OrderItemSerializer
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        items_list = request.data.get('items')
        if items_list:
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            objects_created = 0
            for order_item in items_list:
                order_item.update({'order': basket.id})
                serializer = self.serializer_class(data=order_item)
                if serializer.is_valid():
                    try:
                        serializer.save()
                        objects_created += 1
                    except IntegrityError as error:
                        return Response({'Status': False, 'Errors': str(error)})
                else:
                    return Response({'Status': False, 'Errors': serializer.errors})

            return Response({'Status': True, 'Создано объектов': objects_created})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=basket.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return Response({'Status': True, 'Удалено объектов': deleted_count})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    def put(self, request, *args, **kwargs):
        self.serializer_class = OrderItemSerializer
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        items_list = request.data.get('items')
        if items_list:
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            objects_updated = 0
            objects_created = 0
            for order_item in items_list:
                order_item.update({'order': basket.id})
                objects_updated_cur = 0
                if isinstance(order_item['product_info'], int) and isinstance(order_item['quantity'], int):
                    objects_updated_cur = OrderItem.objects.filter(
                        order_id=basket.id,
                        product_info=order_item['product_info']).update(quantity=order_item['quantity'])
                objects_updated += objects_updated_cur
                if not objects_updated_cur:
                    serializer = self.serializer_class(data=order_item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                            objects_created += 1
                        except IntegrityError as error:
                            return Response({'Status': False, 'Errors': str(error)})
                    else:
                        return Response({'Status': False, 'Errors': serializer.errors})

            return Response({'Status': True, 'Обновлено объектов': objects_updated, 'создано': objects_created})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
