from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    """Document management model"""
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('docx', 'Word Document'),
        ('jpg', 'JPEG Image'),
        ('jpeg', 'JPEG Image'),
        ('png', 'PNG Image'),
        ('csv', 'CSV File'),
        ('xlsx', 'Excel Spreadsheet'),
        ('xls', 'Excel Spreadsheet'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file_size = models.IntegerField()  # in bytes
    is_public = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
