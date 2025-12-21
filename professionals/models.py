from django.db import models
from django.contrib.auth.models import User

class Professional(models.Model):
    """Professional service provider model"""
    PROFESSION_TYPES = [
        ('lawyer', 'Lawyer'),
        ('doctor', 'Doctor'),
        ('electrician', 'Electrician'),
        ('mechanic', 'Mechanic'),
        ('trustee', 'Trustee'),
        ('accountant', 'Accountant'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=50, choices=PROFESSION_TYPES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"
