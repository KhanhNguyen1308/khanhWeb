from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')  # Or any subdirectory within 'media'
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # ... other fields you need ...

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='Documents/')  # Adjust 'documents/' as needed
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # ... other fields ...