from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

RFC_FILTERING = 'rfc'
FULL_NAME_FILTERING = 'full_name'
CompanyFiltering_filter_fields = (RFC_FILTERING, FULL_NAME_FILTERING, )


class CompanyFiltering(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view, *args, **kwargs):
        filtering_request = None
        rfc_filtering_request = request.GET.get(RFC_FILTERING, None)
        full_name_filtering_request = request.GET.get(FULL_NAME_FILTERING, None)
        if rfc_filtering_request and rfc_filtering_request.strip() and full_name_filtering_request \
                and full_name_filtering_request.strip():
            filtering_request = (Q(rfc__icontains=rfc_filtering_request) |
                                 Q(full_name__icontains=full_name_filtering_request))
        elif rfc_filtering_request and rfc_filtering_request.strip():
            filtering_request = (Q(rfc__icontains=rfc_filtering_request))
        elif full_name_filtering_request and full_name_filtering_request.strip():
            filtering_request = (Q(full_name__icontains=full_name_filtering_request))
        if filtering_request:
            queryset = queryset.filter(filtering_request)
        return queryset
