from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MembershipRequestSerializer, StateSerializer, SectorSerializer, SCIANSerializer, \
    TariffFractionSerializer, SuburbSerializer, SuburbWithoutZipCodeSerializer, SuburbMunicipalitySerializer, \
    SuburbSimpleSerializer, MembershipRequestAttachment, MembershipRequestAcceptance, MemberSerializer
from ..models import MembershipRequest, State, Municipality, Suburb, Sector, SCIAN, TariffFraction, Member
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status


class MemberView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        qs = Member.objects.all()
        serializer = MemberSerializer(qs, many=True)
        return Response(serializer.data)


class MyMembershipView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        user = self.request.user
        profile = user.profile
        if profile is None:
            raise ValueError('Este usuario no tiene perfil')
        company = profile.my_company
        if company is None:
            raise ValueError('Este usuario no tiene compañia')
        object = company.membership
        if object is None:
            raise ValueError('Esta compañia no tiene afiliación')
        return object

    def get(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        serializer = MemberSerializer(object)
        return Response(serializer.data)


class MembershipRequestsView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        qs = MembershipRequest.objects.all()
        serializer = MembershipRequestSerializer(qs, many=True)
        return Response(serializer.data)


class MembershipRequestAcceptanceView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = MembershipRequestAcceptance(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            return Response(MemberSerializer(member).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyMembershipRequestAttachmentView(APIView):
    serializer_class = MembershipRequestAttachment
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
            object = MembershipRequest.objects.filter(rfc=company.rfc).first()
        return object

    def get(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        serializer = MembershipRequestAttachment(object.attachment.all(), many=True)
        request_serializer = MembershipRequestSerializer(object)
        return Response({
            "attachments": serializer.data,
            "request": request_serializer.data,
        })

    def post(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        file_serializer = MembershipRequestAttachment(data=request.data)
        if file_serializer.is_valid():
            attachments = file_serializer.save()
            errors = []
            for attachment in attachments:
                try:
                    object.add_attachment(attachment)
                except Exception as e:
                    error = {
                        e.args[1]: e.args[0]
                    }
                    attachment.delete()
                    errors.append(error)
            serializer = MembershipRequestAttachment(object.attachment.all(), many=True)
            request_serializer = MembershipRequestSerializer(object)
            return Response({
                "errors": errors,
                "attachments": serializer.data,
                "request": request_serializer.data,
            })
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if not company.can_request_membership:
            raise ValueError('Este usuario no puede solicitar la afiliación')
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
        object = self.get_object(*args, **kwargs)
        serializer = MembershipRequestSerializer(object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        if object.can_submit:
            object.do_submit(user=request.user)
            serializer = MembershipRequestSerializer(object)
            return Response(serializer.data)
        errors = object.submit_errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class StateView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        zip_code = request.GET.get('zip_code', None)
        if zip_code is not None:
            suburb = Suburb.objects.filter(zip_code=zip_code).first()
            serializer = SuburbSerializer(suburb)
            return Response(serializer.data)
        state = request.GET.get('state', None)
        state = None if state is not None and (state.upper() in ['NULL', 'UNDEFINED'] or state.strip()) == '' else state
        municipality = request.GET.get('municipality', None)
        municipality = None if municipality is not None and (municipality.upper() in ['NULL', 'UNDEFINED'] or
                                                             municipality.strip() == '') else municipality
        suburb = request.GET.get('suburb', None)
        suburb = None if suburb is not None and (suburb.upper() in ['NULL', 'UNDEFINED'] or suburb.strip() == '')\
            else suburb
        if state is not None or municipality is not None or suburb is not None:
            serializer = None
            suburbs = Suburb.objects.all()
            if state is not None:
                serializer = SuburbSimpleSerializer
                suburbs = suburbs.filter(municipality__state__name=state)
            if municipality is not None:
                serializer = SuburbMunicipalitySerializer
                suburbs = suburbs.filter(municipality__name=municipality)
            if suburb is not None:
                serializer = SuburbWithoutZipCodeSerializer
                suburbs = suburbs.filter(name=suburb)
            serializer = serializer(suburbs.first())
            return Response(serializer.data)
        queryset = State.objects.all()
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
