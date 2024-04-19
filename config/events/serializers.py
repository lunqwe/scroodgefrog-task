from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, CustomUserManager, Event


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name']

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
        except:
            raise serializers.ValidationError('Email is not registered')
        

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()
    class Meta:
        model = Event
        fields = '__all__'

class CreateEventSerializer(serializers.ModelSerializer):
    organizer_id = serializers.PrimaryKeyRelatedField(source='organizer', queryset=User.objects.all())
    class Meta:
        model = Event
        fields = ['organizer_id', 'title', 'description', 'date', 'location']


class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']

    

class DeleteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def delete(self):
        self.instance.delete()

class EventRegisterSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
