from django.db import models
from django.utils import timezone

class SiteInfo(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='site/')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return self.name

class SliderImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='slider/')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Partner(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    description = models.TextField()
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    role = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author}"

class Leader(models.Model):
    POSITION_CHOICES = [
        ('Chairperson', 'Chairperson'),
        ('Vice Chairperson', 'Vice Chairperson'),
        ('Organising Secretary', 'Organising Secretary'),
        ('Secretary ', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('IT Manager', 'IT Manager'),
        ('Class Representative', 'Class Representative'),
        # Add more positions as needed
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    image = models.ImageField(upload_to='leaders/')
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.IntegerField(default=0, help_text="Order of display (lower numbers show first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'position']
        verbose_name = 'Leader'
        verbose_name_plural = 'Leaders'
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
# In your models.py
class Constitution(models.Model):
    title = models.CharField(max_length=200, default="KARUASA Constitution")
    document = models.FileField(upload_to='documents/')  # This will store in media/documents/
    version = models.CharField(max_length=20, default="1.0")
    effective_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} v{self.version}"

    class Meta:
        ordering = ['-effective_date']

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"