from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import authenticate

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email','phone_no','is_email_verified')
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'email', 'password', 'phone_no')

    def validate_email(self, value):
        print(value)
        user = CustomUser.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class CurrentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email','phone_no','is_email_verified')
