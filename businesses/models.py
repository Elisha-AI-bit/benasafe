from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    """Business/Partnership model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100)
    ownership_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    pacra_number = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"
