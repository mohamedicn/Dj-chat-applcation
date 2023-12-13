from.serializer import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView ,RetrieveUpdateAPIView
from.models import Profile
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer,RegisterSerializer,LoginSerializer,ProfileSerializer,Emailreset,Emailreset_set
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from.tokens import accout_actvation_token
from django.conf import settings
# this is api decomation
# http://127.0.0.1:6589/api-documentation/

    
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        return Response()

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
class ProfileAPi(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        profile = get_object_or_404(Profile, slug=slug)
        if request.user.id == profile.user.id:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({'message': 'You do not have permission to view this profile.'}, status=status.HTTP_403_FORBIDDEN)

class ProfileAPIUpdate(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Profile, slug=slug)

    def get(self, request, *args, **kwargs):
        profile = self.get_object()

        if request.user.id == profile.user.id:
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        else:
            return Response({'message': 'You do not have permission to view this profile.'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if request.user.id != instance.user.id:
            return Response({'message': 'You do not have permission to update this profile.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class password_reset(generics.GenericAPIView):
    serializer_class=Emailreset
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data["email"]
        user= User.objects.get(email=email)
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = accout_actvation_token.make_token(user)
            user_profile = Profile.objects.get(user=user)
            user_profile.Token = str(uid) + '/' + token
            user_profile.save()
            mail_subject = 'Change A Password'
            message = f"Hi {user.username},\n\nPlease click on the following link to Change your Password\n\n{get_current_site(request).domain}/accounts/api/password_reset_set/{uid}/{token}/\n\nThanks!\n"
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])
            return Response({'detail': 'Email sent successfully. Check your inbox to reset your password.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': f'User with email {email} not found.'}, status=status.HTTP_200_OK)

class password_reset_set(generics.GenericAPIView):
    serializer_class=Emailreset_set
    def post(self,request,uidb64, token):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = str(uidb64) + '/' + token
        try:
            userw = Profile.objects.get(Token=key)
        except Profile.DoesNotExist:
            return Response({'detail': 'No account bt this Email .. Register Now !!'}, status=status.HTTP_200_OK)
        if request.method == 'POST':
            password = request.POST['password']
            passwordconfigration = request.POST['passwordconfigration']
            user = User.objects.get(username=userw.user)
            if 'password' in request.POST: password=request.POST['password']
            else : return Response({'detail': 'Error in ypur password'}, status=status.HTTP_200_OK)
            
            if 'passwordconfigration' in request.POST: passwordconfigration=request.POST['passwordconfigration']
            else : return Response({'detail': 'Error in ypur password'}, status=status.HTTP_200_OK)
            if password and passwordconfigration:
                if password != passwordconfigration:
                    
                    return Response({'detail': 'The two password fields didn’t match.'}, status=status.HTTP_200_OK)
                else:
                    user = userw.user
                    user.set_password(password)
                    user.save()
                    userw.Token = None
                    userw.save()
                    return Response({'detail': 'password reset successfully !'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid token ! try to send message to your mail again !!'}, status=status.HTTP_200_OK)
