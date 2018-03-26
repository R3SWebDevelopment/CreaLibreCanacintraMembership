from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import HealthCheckSerializer
from rest_framework.permissions import AllowAny


class HealthCheckView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response(HealthCheckSerializer({}).data, status=status.HTTP_202_ACCEPTED)
