from django.db import models
from django.contrib.auth.models import User

class Verification(models.Model):
    """Document verification model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE)
    document = models.ForeignKey('assets.AssetDocument', on_delete=models.CASCADE)
    verifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verifications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.asset.name} - {self.status}"
