from django.conf.urls import include, url

from .views import (
    GeneratePDF, ViewAttachmentPDF
)


urlpatterns = [
    url(r'^form_pdf/$', GeneratePDF.as_view(), name='generate_membership_request'),
    url(r'^attachment/view/(?P<id>[0-9]+)/$', ViewAttachmentPDF.as_view(), name='membership_request_attachment_view')
]
