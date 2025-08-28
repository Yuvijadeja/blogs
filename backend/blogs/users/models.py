from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    dob = models.DateField(null=True, blank=True)  # Date of birth
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ], null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username
