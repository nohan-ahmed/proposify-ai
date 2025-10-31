from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils.text import slugify
# Local imports
from .managers import CustomUserManager
from core.choices import LevelChoices
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
    
class UserSkill(models.Model):
    user = models.ForeignKey(to=User, related_name='user_skills', on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='skill_logos', blank=True, null=True)
    skill = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=100, choices=LevelChoices.choices, default=LevelChoices.BEGINNER)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['skill']

    def save(self, *args, **kwargs):
        # Automatically generate slug from skill name and user ID if not provided
        if not self.slug:
            base_slug = slugify(self.skill)
            self.slug = f"{base_slug}-{self.user.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.skill} ({self.level})"