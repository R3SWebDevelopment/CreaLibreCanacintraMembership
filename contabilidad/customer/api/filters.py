from rest_framework import filters
from django.db.models import Q


class ProductServicesFilter(filters.SearchFilter):

    def filter_queryset(self, request, queryset, *args, **kwargs):
        search_term = request.query_params.get('search', None)
        if search_term is not None:
            return queryset.filter(Q(code__icontains=search_term) | Q(name__icontains=search_term))
        return queryset


