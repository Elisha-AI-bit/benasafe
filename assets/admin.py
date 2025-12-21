from django.contrib import admin
from .models import (
    Asset, BankAccount, Insurance, VillageBankingGroup,
    HouseLand, MotorVehicle, Project, GeneralAsset,
    TreasuryBond, IPRights, AssetDocument
)

class AssetDocumentInline(admin.TabularInline):
    model = AssetDocument
    extra = 0
    readonly_fields = ('upload_date', 'file_size')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'asset_type', 'value', 'created_at', 'is_active')
    list_filter = ('asset_type', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AssetDocumentInline]

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('asset', 'bank_name', 'branch_name', 'account_number')
    search_fields = ('asset__name', 'bank_name', 'account_number')

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('asset', 'policy_number', 'provider_name', 'premium_amount')
    search_fields = ('asset__name', 'policy_number', 'provider_name')

@admin.register(MotorVehicle)
class MotorVehicleAdmin(admin.ModelAdmin):
    list_display = ('asset', 'make', 'model', 'year', 'registration_number')
    search_fields = ('asset__name', 'make', 'model', 'registration_number')

@admin.register(HouseLand)
class HouseLandAdmin(admin.ModelAdmin):
    list_display = ('asset', 'plot_number', 'title_deed_number')
    search_fields = ('asset__name', 'plot_number', 'physical_address')

# Register other models
admin.site.register(VillageBankingGroup)
admin.site.register(Project)
admin.site.register(GeneralAsset)
admin.site.register(TreasuryBond)
admin.site.register(IPRights)
