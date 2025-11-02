from django.contrib import admin
from . models import LLM

# Register your models here.


@admin.register(LLM)
class LLMAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'provider', 'provider_model', 'api_endpoint', 'tokens_per_request', 'max_tokens', 'active', 'created_at', 'updated_at')
    list_filter = ('provider', 'active', 'created_at', 'updated_at')
    search_fields = ('name', 'provider', 'provider_model', 'api_endpoint')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    