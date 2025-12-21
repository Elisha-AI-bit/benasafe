from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'file_type', 'file_size', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('title', 'user__username', 'description')
    readonly_fields = ('uploaded_at', 'updated_at', 'file_size')
