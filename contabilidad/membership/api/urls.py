from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MyMembershipRequestView

urlpatterns = [
    url(r'^mine/$', MyMembershipRequestView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)