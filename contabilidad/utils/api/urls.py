from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import HealthCheckView

urlpatterns = [
    url(r'^health_check/$', HealthCheckView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)