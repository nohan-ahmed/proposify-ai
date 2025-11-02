from django.contrib import admin
from .models import Plan, UserCredit
from .forms import PlanAdminForm
# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    form = PlanAdminForm
    list_display = ('id', 'name', 'regular_price', 'discount_price', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('regular_price', 'discount_price')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    


@admin.register(UserCredit)
class UserCreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'credits', 'reserved_credits', 'is_active', 'created_at', 'updated_at')
    list_filter = ('credits', 'reserved_credits', 'is_active')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)