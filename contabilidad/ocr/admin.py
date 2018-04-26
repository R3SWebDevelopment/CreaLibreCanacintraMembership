from django.contrib import admin
from .models import OCRRequest


@admin.register(OCRRequest)
class OCRRequestAdmin(admin.ModelAdmin):

    fields = ['image']
