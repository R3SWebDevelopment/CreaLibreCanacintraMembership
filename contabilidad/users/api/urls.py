from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CommentView

urlpatterns = [
    url(r'^comments/$', CommentView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
