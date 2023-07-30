from rest_framework import viewsets
from rest_framework import serializers


class CustomViewSet(viewsets.ViewSet):
    serializer_class = serializers.Serializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
