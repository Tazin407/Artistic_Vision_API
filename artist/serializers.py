from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model, get_user


User= get_user_model()

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= '__all__'
    
class RegistrationSerializer(serializers.ModelSerializer):
    password= serializers.CharField(label='Password',  style={'input_type': 'password'})
    confirm_password= serializers.CharField( style={'input_type': 'password'})

    class Meta:
        model= User
        fields= [  'first_name','last_name','username', 'email', 'password','confirm_password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'username',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
        }
        
    def is_validated(self, *args, **kwargs):
        email= self.validated_data.get('email')
        username= self.validated_data.get('username')
        password= self.validated_data.get('password')
        confirm_password= self.validated_data.get('confirm_password')
        
        
        if User.objects.filter(email=email).exists:
            raise serializers.ValidationError('This Email Already Exists')
        
        if User.objects.filter(username= username).exists:
            raise serializers.ValidationError('Artist with this username already exists')
        
        if password != confirm_password:
            raise serializers.ValidationError("Passwords Doesn't match")
        
        
        if len(password) < 8:
            raise serializers.ValidationError("Password must have at least 8 characters")
        
        return super().clean(*args, **kwargs)
        
        
    def create(self, validated_data):
        data= validated_data.pop('confirm_password')
        return User.objects.create(**validated_data)
    
    
class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField(required=True)
    password= serializers.CharField(required=True, style={'input_type':'password'})