from rest_framework import routers
from .views import CompanyViewSet, ProductServicesView
from django.conf.urls import url

router = routers.SimpleRouter()

router.register(r'company', CompanyViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^product_service/$', ProductServicesView.as_view()),
]
