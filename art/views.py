from typing import Any
from django.shortcuts import render,redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth.mixins import LoginRequiredMixin
from .import serializers
from .import models
from rest_framework.response import Response
from django.http import HttpResponse


class Artworks(ModelViewSet):
    serializer_class= serializers.ShowArts
    queryset= models.Art.objects.all()
    
    def get_queryset(self):
        queryset= super().get_queryset()
        artist= self.request.query_params.get('artist')
        if artist:
            queryset= queryset.filter(artist= artist)
        
        return queryset
            
    
    
    
class Like(ModelViewSet, LoginRequiredMixin):
    serializer_class= serializers.LikeSerializer
    queryset= models.Like.objects.all()
    
    def create(self, request):
        serializer= self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user= serializer.validated_data.get("artist")
            art= serializer.validated_data.get("art")
            
            try:
                existingLike= models.Like.objects.get(art=art, artist=user)
                existingLike.delete()
                art.likes-=1
                art.save()
                # existingLike.save()
                
                return Response ("Like Removed")
            
            except models.Like.DoesNotExist:
                newLike= serializer.save()
                newLike.save()
                art.likes+=1
                art.save()
                return Response("liked")
                
            
        return Response(serializer.errors)