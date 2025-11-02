from django import forms
from .models import Plan
# Register your models here.

class PlanAdminForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        regular_price = cleaned_data.get('regular_price')
        discount_price = cleaned_data.get('discount_price')
        
        if regular_price and discount_price and regular_price < discount_price:
            raise forms.ValidationError('Regular price must be greater than or equal to the discount price.')
        
        return cleaned_data