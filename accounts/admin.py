from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, UserRole, Bouquet

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'price', 'max_assets_per_category', 'max_beneficiaries', 'max_dependents', 'has_reward_tracker', 'is_active')
    list_filter = ('is_active', 'has_reward_tracker')
    search_fields = ('name', 'display_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'display_name', 'description', 'price', 'is_active')
        }),
        ('Feature Limits', {
            'fields': ('max_assets_per_category', 'max_dependents', 'max_beneficiaries')
        }),
        ('Premium Features', {
            'fields': ('has_reward_tracker', 'reward_percentage')
        }),
        ('Permissions', {
            'fields': ('can_export_reports', 'can_download_documents', 'can_manage_businesses', 'can_manage_professional_contacts')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_type', 'sub_role', 'is_active')
    list_filter = ('role_type', 'sub_role', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role_type', 'sub_role', 'description', 'is_active')
        }),
        ('Admin Permissions', {
            'fields': ('can_manage_users', 'can_assign_bouquets', 'can_view_all_data', 'can_manage_payments', 'can_manage_verification', 'can_export_reports', 'can_approve_documents', 'can_send_notifications'),
            'classes': ('collapse',)
        }),
        ('Verifier Permissions', {
            'fields': ('can_view_pending_verifications', 'can_review_approve', 'can_download_documents', 'can_upload_verification_report', 'can_maintain_audit_log', 'can_notify_users'),
            'classes': ('collapse',)
        }),
        ('Standard User Permissions', {
            'fields': ('can_add_edit_personal_details', 'can_add_spouse_dependents', 'can_upload_documents', 'can_manage_assets', 'can_manage_liabilities', 'can_manage_businesses', 'can_manage_professional_contacts', 'can_add_beneficiaries', 'can_view_dashboard', 'can_receive_verification_updates'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone', 'nrc', 'date_of_birth', 'address', 'profile_picture')
        }),
        ('Role & Subscription', {
            'fields': ('role', 'bouquet', 'subscription_active', 'subscription_start_date', 'subscription_end_date')
        }),
        ('Verification', {
            'fields': ('verification_status', 'is_email_verified')
        })
    )

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role', 'get_bouquet', 'get_verification_status')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'userprofile__role', 'userprofile__bouquet', 'userprofile__verification_status')
    
    def get_role(self, obj):
        return obj.userprofile.role.name if obj.userprofile.role else 'No Role'
    get_role.short_description = 'Role'
    
    def get_bouquet(self, obj):
        return obj.userprofile.bouquet.display_name if obj.userprofile.bouquet else 'No Bouquet'
    get_bouquet.short_description = 'Bouquet'
    
    def get_verification_status(self, obj):
        return obj.userprofile.get_verification_status_display() if obj.userprofile else 'Unknown'
    get_verification_status.short_description = 'Verification Status'

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'bouquet', 'verification_status', 'is_email_verified', 'subscription_active', 'created_at')
    list_filter = ('role', 'bouquet', 'verification_status', 'is_email_verified', 'subscription_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'nrc')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone', 'nrc', 'date_of_birth', 'address', 'profile_picture')
        }),
        ('Role & Subscription', {
            'fields': ('role', 'bouquet', 'subscription_active', 'subscription_start_date', 'subscription_end_date')
        }),
        ('Verification', {
            'fields': ('verification_status', 'is_email_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
