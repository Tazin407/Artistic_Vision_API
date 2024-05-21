from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model, get_user
from .import models

class ShowArts(serializers.ModelSerializer):
    class Meta:
        model= models.Art
        fields= '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Like
        fields= '__all__'