from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MyMembershipRequestView, StateView, SectorView, SCIANView, TariffFractionView, \
    MyMembershipRequestAttachmentView, MembershipRequestAcceptanceView, MembershipRequestsView, MemberView

urlpatterns = [
    url(r'^request/$', MyMembershipRequestView.as_view()),
    url(r'^members/$', MemberView.as_view()),
    url(r'^requests/$', MembershipRequestsView.as_view()),
    url(r'^requests/acceptance/$', MembershipRequestAcceptanceView.as_view()),
    url(r'^request/attachment/$', MyMembershipRequestAttachmentView.as_view()),
    url(r'^states/$', StateView.as_view()),
    url(r'^sector/$', SectorView.as_view()),
    url(r'^scian/$', SCIANView.as_view()),
    url(r'^tariff_fraction/$', TariffFractionView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
