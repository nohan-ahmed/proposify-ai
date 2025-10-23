from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
# Local imports
from .managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # Add additional fields
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = CountryField()
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    
    USERNAME_FIELD = 'email' # Set email as the primary identifier
    REQUIRED_FIELDS = ['username'] # Add username as a required field for registration
    
    # Use the custom user manager
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username