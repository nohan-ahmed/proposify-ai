from django.contrib import admin
from .models import Plan
from .forms import PlanAdminForm
# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    form = PlanAdminForm
    list_display = ('id', 'name', 'regular_price', 'discount_price', 'created_at', 'updated_at')
    list_filter = ('regular_price', 'discount_price')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    