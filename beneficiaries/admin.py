from django.contrib import admin
from .models import Beneficiary

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'relationship', 'phone', 'created_at')
    list_filter = ('relationship', 'created_at')
    search_fields = ('name', 'user__username', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
