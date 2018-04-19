from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MyMembershipRequestView, StateView

urlpatterns = [
    url(r'^$', MyMembershipRequestView.as_view()),
    url(r'^states/$', StateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)