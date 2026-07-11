# core/admin.py
from django.contrib import admin
from .models import SoftwareLicense

@admin.register(SoftwareLicense)
class SoftwareLicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'plan_tier', 'payment_status', 'purchase_date')
    list_filter = ('plan_tier', 'purchase_date')
    search_fields = ('name', 'email')