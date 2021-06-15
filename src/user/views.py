import logging
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger('django')


class HelloWorldAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'message': 'Hello world'
        }, status=status.HTTP_200_OK)
