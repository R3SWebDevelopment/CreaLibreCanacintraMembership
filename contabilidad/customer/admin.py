from django.contrib import admin
from .models import Company, ProductService, Certification


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductService)
class ProductServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    pass
