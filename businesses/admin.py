from django.contrib import admin
from .models import Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'business_type', 'ownership_percentage', 'created_at')
    list_filter = ('business_type', 'created_at')
    search_fields = ('name', 'user__username', 'pacra_number')
    readonly_fields = ('created_at', 'updated_at')
