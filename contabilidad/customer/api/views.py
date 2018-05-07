from rest_framework import viewsets
from rest_framework.decorators import detail_route
from .serializers import CompanySerializer, Company, AddCollaboratorsSerializer, ProductServiceSerializer
from rest_framework.response import Response
from rest_framework import status
from .permissions import AdminAndCollaboratorPermission
from .filterings import CompanyFiltering, CompanyFiltering_filter_fields
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext as _
from rest_framework.generics import ListAPIView
from ..models import ProductService
from rest_framework.permissions import AllowAny
from .filters import ProductServicesFilter


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get', 'post', 'patch']
    permission_classes = (AdminAndCollaboratorPermission, IsAuthenticated)
    filter_backends = (CompanyFiltering,)
    filter_fields = CompanyFiltering_filter_fields

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return super(CompanyViewSet, self).get_queryset(*args, **kwargs)
        return user.companies.all()

    @detail_route(methods=['post'])
    def add_collaborators(self, request, *args, **kwargs):
        company = self.get_object()
        data_serializer = AddCollaboratorsSerializer(request.data)
        new_collaborators = data_serializer.get_users().\
            exclude(pk__in=company.collaborators.all().values_list('id', flat=True))

        if new_collaborators.exists():
            company.collaborators.add(*list(new_collaborators))
            object_serializer = self.get_serializer_class()(company)
            return Response(object_serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": _("No user selected nor is already a collaborator nor valid user")
        }, status=status.HTTP_403_FORBIDDEN)


class ProductServicesView(ListAPIView):
    queryset = ProductService.objects.all()
    serializer_class = ProductServiceSerializer
    permission_classes = (AllowAny,)
    search_fields = ('search', 'name',)
    filter_backends = (ProductServicesFilter,)

