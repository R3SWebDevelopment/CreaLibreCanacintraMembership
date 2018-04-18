from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MembershipRequestSerializer
from ..models import MembershipRequest, Member
from rest_framework.permissions import IsAuthenticated


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

    def get(self, request, format=None, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        serializer = MembershipRequestSerializer(object)
        return Response(serializer.data)
