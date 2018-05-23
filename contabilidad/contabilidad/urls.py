from django.utils.translation import ugettext as _
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken import views
from django.conf import settings

from users.api.views import FacebookLogin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

schema_view = get_swagger_view(title=_('Accounting API'))

urlpatterns = [
    url("^admin/", admin.site.urls),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    # url(r'^ocr/', include('ocr.api.urls', namespace='ocr_api')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^customer/', include('customer.api.urls', namespace='customer_api')),
    url(r'^membership/', include('membership.api.urls', namespace='membership_api')),
    url(r'^users/', include('users.api.urls', namespace='users_api')),
    url(r'^membership/request/', include('membership.request_urls', namespace='membership_request')),
    url(r'^company/', include('customer.request_urls', namespace='company')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^system/', include('utils.api.urls', namespace='system_api')),
    url(r'^$', schema_view),
    url(r'^avatar/', include('avatar.urls')),
]

if settings.ENABLE_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
