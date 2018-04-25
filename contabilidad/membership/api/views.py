from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MembershipRequestSerializer, StateSerializer, SectorSerializer, SCIANSerializer, \
    TariffFractionSerializer
from ..models import MembershipRequest, State, Sector, SCIAN, TariffFraction
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


class MyMembershipRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        user = self.request.user
        profile = user.profile
        if profile is None:
            raise ValueError('Este usuario no tiene perfil')
        company = profile.my_company
        if company is None:
            raise ValueError('Este usuario no tiene compañia')
        object = company.membership_request
        if object is None:
            object, created = MembershipRequest.objects.get_or_create(rfc=company.rfc)
            if created:
                object.business_name = company.full_name
                object.trade_name = company.full_name
                object.setAddress(**company.address)
                object.save()
        return object

    def get(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        serializer = MembershipRequestSerializer(object)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        print("AQUI")
        print("request: {}".format(dir(request)))
        print("DATA: {}".format(request.data))
        object = self.get_object(*args, **kwargs)
        serializer = MembershipRequestSerializer(object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        queryset = State.objects.all()#.prefetch_related('municipality', 'municipality__suburb')
        serializer = StateSerializer(queryset, many=True)
        return Response(serializer.data)


class SectorView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = Sector.objects.all()
        serializer = SectorSerializer(queryset, many=True)
        return Response(serializer.data)


class SCIANView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = SCIAN.objects.all()
        serializer = SCIANSerializer(queryset, many=True)
        return Response(serializer.data)


class TariffFractionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = TariffFraction.objects.all()
        serializer = TariffFractionSerializer(queryset, many=True)
        return Response(serializer.data)
