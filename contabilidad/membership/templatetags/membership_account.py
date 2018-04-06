from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_signup_verification_link(user, key):
    url = '{domain}{path}{key}/'.format(
        domain=settings.CLIENT_APP_DOMAIN,
        path=settings.FRONT_END_SIGNUP_VERIFICATION_URL,
        key=key)
    return url
