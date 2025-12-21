from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Bouquet, UserRole

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    nrc = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'NRC Number'
        })
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Date of Birth'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address',
            'rows': 3
        })
    )
    bouquet = forms.ModelChoiceField(
        queryset=Bouquet.objects.filter(is_active=True),
        empty_label="Select a bouquet",
        required=True,
        help_text="Choose your subscription plan",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes and placeholders to all fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
        
        # Set default bouquet to Blue if available
        try:
            blue_bouquet = Bouquet.objects.get(name='blue', is_active=True)
            self.fields['bouquet'].initial = blue_bouquet
        except Bouquet.DoesNotExist:
            pass

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Get the standard user role
            try:
                standard_role = UserRole.objects.get(role_type='standard', is_active=True)
            except UserRole.DoesNotExist:
                standard_role = None

            # Update or create profile (to avoid conflicts with signal)
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data.get('phone', ''),
                    'nrc': self.cleaned_data.get('nrc', ''),
                    'date_of_birth': self.cleaned_data.get('date_of_birth'),
                    'address': self.cleaned_data.get('address', ''),
                    'bouquet': self.cleaned_data['bouquet'],
                    'role': standard_role
                }
            )

            if not created:
                # Update existing profile
                profile.phone = self.cleaned_data.get('phone', '')
                profile.nrc = self.cleaned_data.get('nrc', '')
                profile.date_of_birth = self.cleaned_data.get('date_of_birth')
                profile.address = self.cleaned_data.get('address', '')
                profile.bouquet = self.cleaned_data['bouquet']
                if not profile.role:
                    profile.role = standard_role
                profile.save()

        return user

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('phone', 'nrc', 'date_of_birth', 'address', 'bouquet', 'profile_picture')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Limit bouquet choices to active bouquets
        self.fields['bouquet'].queryset = Bouquet.objects.filter(is_active=True)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()
        return profile

class AdminUserForm(forms.ModelForm):
    """Form for admin users to manage other users"""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)
    is_active = forms.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ('role', 'bouquet', 'verification_status', 'subscription_active', 'subscription_end_date')
        widgets = {
            'subscription_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            self.fields['is_active'].initial = self.instance.user.is_active
        
        # Limit choices to active roles and bouquets
        self.fields['role'].queryset = UserRole.objects.filter(is_active=True)
        self.fields['bouquet'].queryset = Bouquet.objects.filter(is_active=True)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user information
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.username = self.cleaned_data['username']
            profile.user.is_active = self.cleaned_data['is_active']
            profile.user.save()
            profile.save()
        return profile
