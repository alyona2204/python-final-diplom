from django.db import IntegrityError
from django.db.models import Sum, F
from rest_framework.response import Response

from backend.models import Order
from backend.serializers import OrderSerializer
from backend.signals import new_order
from backend.views.base import CustomViewSet


class OrderView(CustomViewSet):
    serializer_class = OrderSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        order = Order.objects.filter(user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        order_instance = order.filter(id=pk).first()
        if order_instance:
            serializer = self.serializer_class(order_instance)
            return Response(serializer.data)

        return Response({'Status': False, 'Error': 'Товар не найден'}, status=404)


    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        order = Order.objects.filter(user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = self.serializer_class(order, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        order_id = request.data.get('id')
        contact_id = request.data.get('contact')

        if order_id and order_id.isdigit() and contact_id:
            try:
                is_updated = Order.objects.filter(
                    user_id=request.user.id, id=order_id).update(
                    contact_id=contact_id,
                    state='new')
            except IntegrityError as error:
                print(error)
                return Response({'Status': False, 'Errors': 'Неправильно указаны аргументы'})
            else:
                if is_updated:
                    new_order.send(sender=self.__class__, user_id=request.user.id)
                return Response({'Status': True})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
