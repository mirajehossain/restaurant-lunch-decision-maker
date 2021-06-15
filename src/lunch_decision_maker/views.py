from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny


class HealthCheckAPI(APIView):
    permission_classes = (AllowAny, )

    def get(self, request: Request) -> Response:
        data = {
            'message': 'Lunch Decision Maker Service API.',
            'method': str(self.request.method).lower(),
        }
        return Response(data={'data': data}, status=status.HTTP_200_OK)
