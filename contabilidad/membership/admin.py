from django.contrib import admin
from .models import MembershipRequest, Member, State, Municipality, Suburb, Sector, Branch, SCIAN, TariffFraction, \
    AttachedFile
from django.core.urlresolvers import reverse
from django.utils.text import force_text
from django.utils.translation import ugettext_lazy as _


@admin.register(AttachedFile)
class AttachedFileAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    pass


class MunicipalityInline(admin.TabularInline):
    model = Municipality
    fields = ('name', 'get_edit_link',)
    readonly_fields = ('name', 'get_edit_link', )

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return """<a href="{url}">{text}</a>""".format(
                url=url,
                text=_("Edit this %s separately") % obj._meta.verbose_name,
            )
        return _("(save and continue editing to create a link)")
    get_edit_link.short_description = _("Edit link")
    get_edit_link.allow_tags = True


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    inlines = [
        MunicipalityInline,
    ]


class SuburbInline(admin.TabularInline):
    model = Suburb
    fields = ('name', 'zip_code', 'get_edit_link',)
    readonly_fields = ('name', 'zip_code', 'get_edit_link',)

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return """<a href="{url}">{text}</a>""".format(
                url=url,
                text=_("Edit this %s separately") % obj._meta.verbose_name,
            )
        return _("(save and continue editing to create a link)")
    get_edit_link.short_description = _("Edit link")
    get_edit_link.allow_tags = True


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    inlines = [
        SuburbInline,
    ]


@admin.register(Suburb)
class SuburbAdmin(admin.ModelAdmin):
    pass


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(SCIAN)
class SCIANAdmin(admin.ModelAdmin):
    pass


@admin.register(TariffFraction)
class TariffFractionAdmin(admin.ModelAdmin):
    pass
