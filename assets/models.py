from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Asset(models.Model):
    """Base asset model"""
    ASSET_TYPES = [
        ('bank_account', 'Bank Account'),
        ('insurance', 'Insurance & Social Security'),
        ('village_banking', 'Village Banking Group'),
        ('house_land', 'House/Land'),
        ('motor_vehicle', 'Motor Vehicle'),
        ('project', 'Project'),
        ('general_asset', 'General Asset'),
        ('treasury_bond', 'Treasury Bond'),
        ('ip_rights', 'IP Rights'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class BankAccount(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50, blank=True)

class Insurance(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=100)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)

class VillageBankingGroup(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    chilimba_name = models.CharField(max_length=100)
    chairperson_name = models.CharField(max_length=100)
    chairperson_phone = models.CharField(max_length=20)
    treasurer_name = models.CharField(max_length=100)
    treasurer_phone = models.CharField(max_length=20)
    meeting_frequency = models.CharField(max_length=50, blank=True)

class HouseLand(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    physical_address = models.TextField()
    plot_number = models.CharField(max_length=50, blank=True)
    gps_coordinates = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=50, blank=True)  # e.g., "1 hectare", "500 sqm"
    title_deed_number = models.CharField(max_length=50, blank=True)

class MotorVehicle(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    registration_number = models.CharField(max_length=20)
    chassis_number = models.CharField(max_length=50)
    engine_number = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=30)

class Project(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    progress_status = models.CharField(max_length=50, choices=[
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ], default='planning')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

class GeneralAsset(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)

class TreasuryBond(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    issuer = models.CharField(max_length=100)
    bond_number = models.CharField(max_length=50)
    issue_date = models.DateField()
    maturity_date = models.DateField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    face_value = models.DecimalField(max_digits=15, decimal_places=2)

class IPRights(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=50)
    registration_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    rights_type = models.CharField(max_length=50, choices=[
        ('patent', 'Patent'),
        ('trademark', 'Trademark'),
        ('copyright', 'Copyright'),
        ('design', 'Design'),
    ])

class AssetDocument(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='asset_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10, blank=True)  # pdf, doc, jpg, etc.
    file_size = models.IntegerField(blank=True)  # in bytes
