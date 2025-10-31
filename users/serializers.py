from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
# Local imports
from . import models


# Write you serializers here.

class CustomRegisterSerializer(serializers.ModelSerializer):
    # Add a confirm password field for validation.
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = models.User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, fields):
        # Check if the passwords match.
        if fields['password'] != fields['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Validate the password using Django's built-in validators.
        try:
            validate_password(fields['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return fields
    
    
    def create(self, validated_data):
        # Remove the confirm_password field from the validated data.
        validated_data.pop('confirm_password', None)
        # Set the user as inactive by default.
        validated_data.setdefault('is_active', False)
        # Create the user.
        user = models.User.objects.create_user(**validated_data)
        return user
    
# UserSkill serializer here
class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserSkill
        fields = '__all__'
        read_only_fields = ('id', 'user', 'slug', 'created_at', 'updated_at')