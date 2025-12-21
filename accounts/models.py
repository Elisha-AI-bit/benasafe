from django.db import models
from django.contrib.auth.models import User, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

class Bouquet(models.Model):
    """Subscription bouquet tiers with specific features and limits"""
    name = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Feature limits
    max_assets_per_category = models.IntegerField(default=3)
    max_dependents = models.IntegerField(default=1)
    max_beneficiaries = models.IntegerField(default=3)
    has_reward_tracker = models.BooleanField(default=False)
    reward_percentage = models.IntegerField(default=0, help_text="Reward percentage every 3 years")
    
    # Permissions
    can_export_reports = models.BooleanField(default=True)
    can_download_documents = models.BooleanField(default=True)
    can_manage_businesses = models.BooleanField(default=True)
    can_manage_professional_contacts = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.display_name} - ${self.price}"

class UserRole(models.Model):
    """User roles with specific permissions and access levels"""
    ROLE_TYPES = [
        ('admin', 'Admin'),
        ('verifier', 'Verifier'),
        ('standard', 'Standard User'),
    ]
    
    ADMIN_SUB_ROLES = [
        ('super_admin', 'SuperAdmin'),
        ('admin_staff', 'Admin Staff'),
    ]
    
    VERIFIER_SUB_ROLES = [
        ('corporate_verifier', 'Corporate Verifier'),
        ('legal_verifier', 'Legal Verifier'),
    ]

    name = models.CharField(max_length=50, unique=True)
    role_type = models.CharField(max_length=20, choices=ROLE_TYPES)
    sub_role = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    
    # Admin permissions
    can_manage_users = models.BooleanField(default=False)
    can_assign_bouquets = models.BooleanField(default=False)
    can_view_all_data = models.BooleanField(default=False)
    can_manage_payments = models.BooleanField(default=False)
    can_manage_verification = models.BooleanField(default=False)
    can_export_reports = models.BooleanField(default=False)
    can_approve_documents = models.BooleanField(default=False)
    can_send_notifications = models.BooleanField(default=False)
    
    # Verifier permissions
    can_view_pending_verifications = models.BooleanField(default=False)
    can_review_approve = models.BooleanField(default=False)
    can_download_documents = models.BooleanField(default=False)
    can_upload_verification_report = models.BooleanField(default=False)
    can_maintain_audit_log = models.BooleanField(default=False)
    can_notify_users = models.BooleanField(default=False)
    
    # Standard user permissions
    can_add_edit_personal_details = models.BooleanField(default=True)
    can_add_spouse_dependents = models.BooleanField(default=True)
    can_upload_documents = models.BooleanField(default=True)
    can_manage_assets = models.BooleanField(default=True)
    can_manage_liabilities = models.BooleanField(default=True)
    can_manage_businesses = models.BooleanField(default=True)
    can_manage_professional_contacts = models.BooleanField(default=True)
    can_add_beneficiaries = models.BooleanField(default=True)
    can_view_dashboard = models.BooleanField(default=True)
    can_receive_verification_updates = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['role_type', 'name']

    def __str__(self):
        return f"{self.get_role_type_display()} - {self.name}"

    def clean(self):
        # Ensure sub_role is provided for admin and verifier roles
        if self.role_type in ['admin', 'verifier'] and not self.sub_role:
            raise ValidationError(f"Sub-role is required for {self.get_role_type_display()} roles")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    nrc = models.CharField(max_length=20, blank=True)  # National Registration Card
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    # Role and subscription
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT, null=True, blank=True)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.PROTECT, null=True, blank=True)
    
    # Profile information
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    
    # Subscription details
    subscription_active = models.BooleanField(default=True)
    subscription_start_date = models.DateField(auto_now_add=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    
    # Verification status
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('not_required', 'Not Required'),
        ],
        default='pending'
    )
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        role_name = self.role.name if self.role else "No Role"
        bouquet_name = self.bouquet.display_name if self.bouquet else "No Bouquet"
        return f"{self.user.username} - {role_name} - {bouquet_name}"

    @property
    def is_admin(self):
        return self.role and self.role.role_type == 'admin'

    @property
    def is_verifier(self):
        return self.role and self.role.role_type == 'verifier'

    @property
    def is_standard_user(self):
        return self.role and self.role.role_type == 'standard'

    @property
    def is_super_admin(self):
        return self.role and self.role.role_type == 'admin' and self.role.sub_role == 'super_admin'

    def has_permission(self, permission_name):
        """Check if user has a specific permission based on their role"""
        if not self.role:
            return False
        
        # Check if the permission attribute exists on the role
        return getattr(self.role, permission_name, False)

    def get_asset_limit(self, category=None):
        """Get asset limit based on bouquet"""
        if not self.bouquet:
            return 0
        return self.bouquet.max_assets_per_category

    def get_beneficiary_limit(self):
        """Get beneficiary limit based on bouquet"""
        if not self.bouquet:
            return 0
        return self.bouquet.max_beneficiaries

    def get_dependent_limit(self):
        """Get dependent limit based on bouquet"""
        if not self.bouquet:
            return 0
        return self.bouquet.max_dependents

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile with default role and bouquet
        try:
            standard_role = UserRole.objects.get(role_type='standard', is_active=True)
            blue_bouquet = Bouquet.objects.get(name='blue', is_active=True)
            UserProfile.objects.create(
                user=instance,
                role=standard_role,
                bouquet=blue_bouquet
            )
        except (UserRole.DoesNotExist, Bouquet.DoesNotExist):
            # Fallback: create profile without role/bouquet if defaults don't exist
            UserProfile.objects.create(user=instance)
    else:
        # For existing users, save the profile if it exists
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
