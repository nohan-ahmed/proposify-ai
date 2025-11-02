from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Subsctiption)
class SubsctiptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'status', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'plan')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')