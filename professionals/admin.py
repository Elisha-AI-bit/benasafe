from django.contrib import admin
from .models import Professional

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'profession', 'phone', 'created_at')
    list_filter = ('profession', 'created_at')
    search_fields = ('name', 'user__username', 'phone', 'company')
    readonly_fields = ('created_at', 'updated_at')
