from django.conf.urls import include, url

from .views import (
    GeneratePDF
)


urlpatterns = [
    url(r'^form_pdf/$', GeneratePDF.as_view(), name='generate_membership_request')
]
