from django.contrib import admin
from django.utils.html import format_html
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



@admin.register(models.UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'skill', 'level', 'logo_preview', 'created_at', 'updated_at')
    list_filter = ('level', 'created_at', 'updated_at')
    search_fields = ('user__username', 'skill', 'description')
    ordering = ('skill',)
    readonly_fields = ('created_at', 'updated_at', 'logo_preview')
    prepopulated_fields = {'slug': ('skill',)}

    fieldsets = (
        ("User & Skill Info", {
            'fields': ('user', 'skill', 'level', 'slug')
        }),
        ("Details", {
            'fields': ('description', 'logo', 'logo_preview')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px; border-radius:6px;" />', obj.logo.url)
        return "—"
    logo_preview.short_description = "Logo Preview"


@admin.register(models.UserExperience)
class UserExperienceAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'company', 'position', 'start_date', 'end_date', 'currently_working',)
    list_filter = ('start_date', 'end_date', 'currently_working', 'created_at', 'updated_at')
    search_fields = ('user__username', 'company', 'position', 'description')
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at', 'logo_preview')

    fieldsets = (
        ("User & Experience Info", {
            'fields': ('user', 'company', 'position', 'start_date', 'end_date', 'currently_working')
        }),
        ("Details", {
            'fields': ('description', 'logo', 'logo_preview')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px; border-radius:6px;" />', obj.logo.url)
        return "—"
    logo_preview.short_description = "Logo Preview"
    

@admin.register(models.UserEducation)
class UserEducationAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'institute_name', 'degree', 'start_date', 'end_date', 'currently_studying',)
    list_filter = ('start_date', 'end_date', 'currently_studying', 'created_at', 'updated_at')
    search_fields = ('user__username', 'institute_name', 'degree', 'description')
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at', 'logo_preview')

    fieldsets = (
        ("User & Education Info", {
            'fields': ('user', 'institute_name', 'degree', 'start_date', 'end_date', 'currently_studying')
        }),
        ("Details", {
            'fields': ('description', 'logo', 'logo_preview')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px; border-radius:6px;" />', obj.logo.url)
        return "—"
    logo_preview.short_description = "Logo Preview"