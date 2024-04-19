from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password, full_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return CustomUser.objects.create_user(email=email, username=username, full_name=full_name, password=password, **extra_fields)
    
    def login_user(self, request, user, email, password):
        auth_user = authenticate(request=request, email=email, password=password)
        if auth_user:
            # if user is authenticated
            token, created = Token.objects.get_or_create(user=auth_user)
            return ({'status': 'success', 'token': token.key}, status.HTTP_202_ACCEPTED)
        else:
            # if password or email are invalid
            return ({'status': 'error', 'detail': "Invalid email or password"}, status.HTTP_401_UNAUTHORIZED)
        
        
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, default='')
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Event(models.Model):
    organizer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Організатор'
        )
    title = models.CharField("Назва івенту", max_length=255)
    description = models.TextField('Опис івенту')
    date = models.DateTimeField('Дата і час івенту')
    location = models.TextField('Місце проведення')
    # Також можна реалізувати через models.PointField()
    attendees = models.ManyToManyField(CustomUser, related_name='registered_events')

    def __str__(self) -> str:
        return self.title


