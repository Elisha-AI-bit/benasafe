from django.contrib import admin
from .models import Subscription, Payment

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'start_date', 'end_date')
    list_filter = ('plan', 'is_active', 'start_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'amount', 'status', 'reference', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'reference')
    readonly_fields = ('created_at', 'updated_at')
