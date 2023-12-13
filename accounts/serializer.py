from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from.models import Profile
from.tokens import accout_actvation_token
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from project import settings

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [ "phone", "image", "country",'adress',]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ "first_name", "last_name", "username"]
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email','first_name', 'last_name', 'password', 'password2',
                )
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        user = User.objects.create(
        username=username,
        is_active=False,
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        request = self.context.get('request')
        mailsubject='activate your account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = accout_actvation_token.make_token(user)
        message=f"Hi {user.username},\n\nPlease click on the following link to activate your account:\n\n{get_current_site(request).domain}/accounts/activate_account/{uid}/{token}/\n\nThanks!\n"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email,] 
        emailmessage=send_mail(mailsubject,message,email_from,recipient_list)
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email','password',)
        
        
        # https://www.youtube.com/watch?v=9TBmU_PU32w&ab_channel=OhunayoGege
        
class Emailreset(serializers.Serializer):
    email=serializers.EmailField()
    class Meta:
        fields =('email',)
        
class Emailreset_set(serializers.Serializer):
    password=serializers.CharField()
    passwordconfigration=serializers.CharField()
    class Meta:
        fields =('password','passwordconfigration',)