from rest_framework import serializers
from . import models

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        
class UserCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserCredit
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']