from django.contrib import admin
from .models import MembershipRequest, Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass

@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    pass
