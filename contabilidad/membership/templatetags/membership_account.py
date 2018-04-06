from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def get_signup_verification_link(user, key):
    return 'http://localhost:3000/signup/verification/{}/'.format(key)
