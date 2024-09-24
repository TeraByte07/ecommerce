from rest_framework import serializers
from django.contrib.auth.models import User
from .validators import validate_password_complexity
from django.core.exceptions import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
        
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"}, code='password_mismatch')
        
        # Check if the email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists"}, code='email_exists')

        # Validate the password using custom validators
        try:
            validate_password_complexity(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)}, code='invalid_password')
        
        return data
    
    def create(self, validated_data):
        # Remove password2 as it's not needed for user creation
        validated_data.pop('password2', None)
        # Create user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user