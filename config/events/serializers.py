from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, CustomUserManager


User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'full_name', 'password', 'password2']
        extra_kwargs = {
            "user_id": {'required': True}
        }
        
        
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        else:
            data.pop('password2')
        return data

        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        # if user exists
        try:
            user = get_object_or_404(CustomUser, email=email)
            if user:
                return {"user": user, 'email': email, 'password': password}
        except Exception as e:
            # if user doesn't exists
            data = {'status': 'error', 'detail': "Email is not registered."}
            return data