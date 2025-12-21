from django.contrib import admin
from .models import Verification

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'document', 'status', 'verifier', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'asset__name', 'verifier__username')
    readonly_fields = ('created_at', 'updated_at')
