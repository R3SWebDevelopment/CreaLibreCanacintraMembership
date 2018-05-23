from django.conf.urls import include, url

from .views import (
    ViewAttachmentPDF
)


urlpatterns = [
    url(r'^certification/attachment/view/(?P<id>[0-9]+)/$',
        ViewAttachmentPDF.as_view(),
        name='certification_attachment_view')
]
