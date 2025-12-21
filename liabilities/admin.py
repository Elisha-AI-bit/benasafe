from django.contrib import admin
from .models import Liability

@admin.register(Liability)
class LiabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'liability_type', 'amount', 'due_date', 'created_at')
    list_filter = ('liability_type', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
