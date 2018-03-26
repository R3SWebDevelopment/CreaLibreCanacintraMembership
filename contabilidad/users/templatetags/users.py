from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def get_user(email):
    return User.objects.filter(email__iexact=email).first()
