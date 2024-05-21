from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))
        email= self.normalize_email(email)
        user= self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        if len(email) > 254:
            print("Email address is too long:", email)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
class Artist(AbstractUser):

    username=None
    
    email= models.EmailField(_('Email Address'), unique=True)
    password= models.CharField(max_length=30)
    is_verified= models.BooleanField(default=False)
    username= models.CharField(max_length= 20)
    first_name= models.CharField(max_length=30)
    last_name= models.CharField(max_length=30)
    
    USERNAME_FIELD= 'email'
    
    REQUIRED_FIELDS=['username', 'password']
    
    object= CustomUserManager()
    
    def __str__(self) -> str:
        return self.first_name+" "+self.last_name
    
    
    
        