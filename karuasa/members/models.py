from django.contrib.auth.models import AbstractUser
from django.db import models

class Member(AbstractUser):
    MEMBER_TYPES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('executive', 'Executive'),
    ]
    
    registration_number = models.CharField(max_length=50, unique=True)
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPES)
    phone_number = models.CharField(max_length=15)
    course = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    is_verified = models.BooleanField(default=False)
    mpesa_transaction_code = models.CharField(max_length=50, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.registration_number}"

