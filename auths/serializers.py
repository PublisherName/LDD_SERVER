from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,allow_blank=False)
    confirm_password = serializers.CharField(write_only=True,allow_blank=False)
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    token = models.OneToOneField(Token, on_delete=models.CASCADE, null=True)

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',
                  'confirm_password'
                  )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords do not match.")
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError('Username already exists')
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError('Email already exists')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data['username']
        password = data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError('User is not active')
        else:
            raise ValidationError('Must provide username and password both')
        return data
    
class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    confirm_password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('password','confirm_password','old_password')
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords do not match.")
        if data['password'] == data['old_password']:
            raise ValidationError("New password cannot be same as old password.")
        return data
    
    def update(self, instance, validated_data):
        if not self.instance.check_password(validated_data['old_password']):
            raise ValidationError("Old password is incorrect.")
        instance.set_password(validated_data['password'])
        instance.save()
        return instance