from typing import Any
from django.shortcuts import render,redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from .import serializers
from .import models

from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
# Create your views here.

#email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages

User= get_user_model()

class Artists(ModelViewSet):
    serializer_class= serializers.ArtistSerializer
    queryset= User.objects.all()
    
class RegistrationAPIView(APIView):
    serializer_class= serializers.RegistrationSerializer
  
    def post(self, request):
        serializer= self.serializer_class(data=request.data)        
        if serializer.is_valid():
            
            # print(serializer)
            new_user= serializer.save()
            password= serializer.validated_data.get('password')
            new_user.set_password(password)
            new_user.save()
            print('User saved')
            #sending email
            if new_user.is_verified == False:
                current_site= get_current_site(request)
                user= new_user
                uid= urlsafe_base64_encode(force_bytes(user.pk))
                token= account_activation_token.make_token(user)
                print(uid, token)
                email= user.email
                subject= "Verify Your Email Address"
                message = render_to_string('verifyEmail.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
                
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            print('Email should be sent')
            
            return Response('Please Check Your Email')
        
        else:  
            print(serializer.errors)
        return Response(serializer.errors)
                
    
def activate(request, uidb64, token):
    next= request.GET.get('next')
    print(uidb64, token)
    
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user= None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified=True 
        user.save()
        # messages.success(request,'Your account has been verified successfully')
        return HttpResponse('Your account has been verified successfully. You may proceed to log in.')
    
    return HttpResponse('This email has been verified already')


class LoginView(APIView):
    serializer_class= serializers.LoginSerializer
    
    def post(self, request):
        email= request.data.get('email')
        password= request.data.get('password')
        
        user= authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_verified== True:
                print("verified")
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response('Please click on the link sent in your email')
        
        return Response('Wrong info. Try again')
    
class LogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response('Logged out successfully')


