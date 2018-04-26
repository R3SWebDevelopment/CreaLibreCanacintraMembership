from rest_framework import viewsets

from .serializers import OCRRequestSerializer, OCRRequest


class OCRRequestViewSet(viewsets.ModelViewSet):
    queryset = OCRRequest.objects.all()
    serializer_class = OCRRequestSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self, *args, **kwargs):
        qs = super(OCRRequestViewSet, self).get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return qs
        return qs.filter(created_by = user)
