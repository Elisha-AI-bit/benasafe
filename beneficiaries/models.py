from django.db import models
from django.contrib.auth.models import User

class Beneficiary(models.Model):
    """Beneficiary/Emergency contact model"""
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    nrc = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='beneficiaries/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"
