from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CommentView, ProductsServicesView, CertificationView

urlpatterns = [
    url(r'^comments/$', CommentView.as_view()),
    url(r'^products_services/$', ProductsServicesView.as_view()),
    url(r'^certifications/$', CertificationView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
