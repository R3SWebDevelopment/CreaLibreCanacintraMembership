from django.contrib import admin
from .models import MembershipRequest, Member, State, Municipality, Sector, Branch, SCIAN


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
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
