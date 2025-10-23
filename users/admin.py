from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here. 
    
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the User model.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = models.User

    # List view settings
    list_display = ('id', 'username', 'email', 'country', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'country')
    ordering = ('id',)

    # Field groups for change view
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': (
                'profile_pic',
                'first_name',
                'last_name',
                'phone_number',
                'date_of_birth',
                'country',
                'bio',
                'website',
                'github',
                'twitter',
                'linkedin',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Field groups for add view
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
