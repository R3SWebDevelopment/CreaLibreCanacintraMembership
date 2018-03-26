from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField

from django.contrib.auth.models import User


class Company(models.Model):
    full_name = models.CharField(max_length=250, null=False, blank=False, verbose_name=_('Company name'))
    rfc = models.CharField(max_length=13, name=False, blank=False, unique=True, verbose_name=_('Tax ID'),
                           help_text=_('Use the following format XXX[X]999999XXX'))
    address = JSONField(default={})
    collaborators = models.ManyToManyField(User, related_name='companies', verbose_name=_('Collaborators'))

    class Meta:
        ordering = ['rfc']

    def __str__(self):
        return "{} - {}".format(self.rfc, self.full_name)

    def __unicode__(self):
        return u"{} - {}".format(self.rfc, self.full_name)
