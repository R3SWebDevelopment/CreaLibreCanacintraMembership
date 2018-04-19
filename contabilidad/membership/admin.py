from django.contrib import admin
from .models import MembershipRequest, Member, State, Municipality


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
