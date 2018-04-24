from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import HealthCheckSerializer, CatalogSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class HealthCheckView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response(HealthCheckSerializer({}).data, status=status.HTTP_202_ACCEPTED)


class CatalogView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        return Response(CatalogSerializer({}).data, status=status.HTTP_202_ACCEPTED)