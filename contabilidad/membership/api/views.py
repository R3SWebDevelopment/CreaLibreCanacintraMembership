from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MembershipRequestSerializer


class MyMembershipRequestView(APIView):

    def get(self, request, format=None):
        return Response({})
