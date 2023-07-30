from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework.response import Response
from rest_framework import serializers

from backend.views.base import CustomViewSet


class PartnerUpdateSerializer(serializers.Serializer):
    url = serializers.CharField(
        required=True,
        max_length=255,
        help_text="Урл для загрузки"
    )


class PartnerUpdate(CustomViewSet):
    serializer_class = PartnerUpdateSerializer

    def create(self, request, *args, **kwargs):
        """

        @type request: Request
        """
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return Response({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            url: str = serializer.data['url']
            if url:
                validate_url = URLValidator()
                try:
                    if not url.startswith('http://shop'):
                        validate_url(url)

                    from backend.tasks import get_import
                    get_import.delay(request.user.id, url)
                    return Response({'Status': True})
                except ValidationError as e:
                    return Response({'Status': False, 'Error': str(e)})

        return Response({'error': serializer.errors})