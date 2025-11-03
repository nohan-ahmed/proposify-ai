from rest_framework import serializers
from . import models

class StripeSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField(required=True)
    
    def validate_plan_id(self, value):
        # Add any custom validation for plan_id if necessary
        if not value:
            raise serializers.ValidationError("Plan ID cannot be empty.")
        
        # Add any additional validation for plan_id
        try:
            # Example: Check if the plan exists in the database
            plan = models.Plan.objects.get(id=value)
        except models.Plan.DoesNotExist:
            raise serializers.ValidationError("Invalid Plan ID.")
        
        # Return the validated value
        return value