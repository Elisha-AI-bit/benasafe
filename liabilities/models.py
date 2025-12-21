from django.db import models
from django.contrib.auth.models import User

class Liability(models.Model):
    """Base liability model"""
    LIABILITY_TYPES = [
        ('loan', 'Loan'),
        ('advance', 'Advance'),
        ('refund', 'Refund'),
        ('debt', 'Debt'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liability_type = models.CharField(max_length=20, choices=LIABILITY_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    source = models.CharField(max_length=100, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"
