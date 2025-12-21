from django import forms
from .models import (
    Asset, BankAccount, Insurance, VillageBankingGroup,
    HouseLand, MotorVehicle, Project, GeneralAsset,
    TreasuryBond, IPRights, AssetDocument
)

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    bank_name = forms.CharField(max_length=100, required=True)
    branch_name = forms.CharField(max_length=100, required=True)
    account_name = forms.CharField(max_length=100, required=True)
    account_number = forms.CharField(max_length=50, required=True)
    account_type = forms.CharField(max_length=50, required=False)

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    policy_number = forms.CharField(max_length=100, required=True)
    provider_name = forms.CharField(max_length=100, required=True)
    coverage_type = forms.CharField(max_length=100, required=True)
    premium_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    maturity_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class VillageBankingForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    chilimba_name = forms.CharField(max_length=100, required=True)
    chairperson_name = forms.CharField(max_length=100, required=True)
    chairperson_phone = forms.CharField(max_length=20, required=True)
    treasurer_name = forms.CharField(max_length=100, required=True)
    treasurer_phone = forms.CharField(max_length=20, required=True)
    meeting_frequency = forms.CharField(max_length=50, required=False)

class HouseLandForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    physical_address = forms.CharField(widget=forms.Textarea, required=True)
    plot_number = forms.CharField(max_length=50, required=False)
    gps_coordinates = forms.CharField(max_length=100, required=False)
    size = forms.CharField(max_length=50, required=False)
    title_deed_number = forms.CharField(max_length=50, required=False)

class MotorVehicleForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    make = forms.CharField(max_length=50, required=True)
    model = forms.CharField(max_length=50, required=True)
    year = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'min': 1900, 'max': 2025}))
    registration_number = forms.CharField(max_length=20, required=True)
    chassis_number = forms.CharField(max_length=50, required=True)
    engine_number = forms.CharField(max_length=50, required=False)
    color = forms.CharField(max_length=30, required=True)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    contact_person = forms.CharField(max_length=100, required=True)
    contact_phone = forms.CharField(max_length=20, required=True)
    contact_email = forms.EmailField(required=True)
    progress_status = forms.ChoiceField(choices=[
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ], initial='planning')
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class GeneralAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    serial_number = forms.CharField(max_length=100, required=False)
    manufacturer = forms.CharField(max_length=100, required=False)
    model_number = forms.CharField(max_length=100, required=False)
    purchase_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    warranty_expiry = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class TreasuryBondForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    issuer = forms.CharField(max_length=100, required=True)
    bond_number = forms.CharField(max_length=50, required=True)
    issue_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    maturity_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    interest_rate = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    face_value = forms.DecimalField(max_digits=15, decimal_places=2, required=True)

class IPRightsForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    registration_number = forms.CharField(max_length=50, required=True)
    registration_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    expiry_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    rights_type = forms.ChoiceField(choices=[
        ('patent', 'Patent'),
        ('trademark', 'Trademark'),
        ('copyright', 'Copyright'),
        ('design', 'Design'),
    ], required=True)

class AssetDocumentForm(forms.ModelForm):
    class Meta:
        model = AssetDocument
        fields = ['title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
