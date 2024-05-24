from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model, get_user
from .import models

class ShowArts(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    class Meta:
        model= models.Art
        fields= fields = ['id', 'title', 'image', 'description','likes', 'artist', 'artist_name']
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Like
        fields= '__all__'