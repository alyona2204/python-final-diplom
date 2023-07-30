from django.db.models import Q
from rest_framework.response import Response

from backend.models import Contact
from backend.serializers import ContactSerializer
from backend.views.base import CustomViewSet


class ContactView(CustomViewSet):
    serializer_class = ContactSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        contact = Contact.objects.filter(user_id=request.user.id)
        serializer = self.serializer_class(contact, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'city', 'street', 'phone'}.issubset(request.data):
            post_data = dict(request.data)
            post_data.update({'user': request.user.id})
            serializer = self.serializer_class(data=post_data)

            if serializer.is_valid():
                serializer.save()
                return Response({'Status': True})
            else:
                return Response({'Status': False, 'Errors': serializer.errors})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return Response({'Status': True, 'Удалено объектов': deleted_count})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        contact_id = request.data.get('id')
        if contact_id and contact_id.isdigit():
            contact = Contact.objects.filter(id=contact_id, user_id=request.user.id).first()
            if contact:
                serializer = self.serializer_class(contact, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'Status': True})
                else:
                    return Response({'Status': False, 'Errors': serializer.errors})

        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
