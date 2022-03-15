from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken

from api.models import CustomUser
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer,
         ChangePasswordSerializer, ForgotPasswordSerializer, CurrentLoginSerializer)
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from knox.auth import TokenAuthentication
from django.core.mail import send_mail
from restdemo import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import email_verified_token
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
User = get_user_model() 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes=[permissions.AllowAny]
    serializer_class=UserSerializer

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated], url_name='me',url_path='me')
    def me(self, request,*args, **kwargs):
        return Response({
            "user": CurrentLoginSerializer(request.user, context=self.get_serializer_context()).data
        })

    @action(detail=False, methods=['POST'],serializer_class=LoginSerializer,url_name='userlogin',url_path='login')
    def userlogin(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

    @action(methods=['POST'], detail=False, url_name='userlogout',url_path='logout', permission_classes=[permissions.IsAuthenticated],authentication_classes = (TokenAuthentication,))
    def logout(self, request):
        request._auth.delete()
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False,serializer_class=ChangePasswordSerializer, permission_classes=[permissions.IsAuthenticated], url_name='changepassword',url_path='password_change')
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not request.user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            new_password = serializer.data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            response = {
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'Password updated successfully',
                        'data': []
                    }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False,serializer_class=ForgotPasswordSerializer, url_name='forgetpassword',url_path='password_reset')
    def password_reset(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            associated_users = User.objects.filter(Q(email=user['email']))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Link"
                    email_template_name = "password_reset_email.txt"
                    current_site = get_current_site(request)
                    c = {
                    'domain':current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    message = render_to_string(email_template_name, c)
                    send_mail(subject, message, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                    return HttpResponse('Reset Link has been send to email')
            return HttpResponse('User not found')
        return HttpResponse('data not valid')

    def perform_create(self, user,current_site):
        message = render_to_string('acc_active_email.html', {
            'user':user, 
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verified_token.make_token(user),
        })
        subject = 'Activate your account.'
        send_mail(subject=subject ,message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user],  fail_silently=False,)
    
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(request)
        self.perform_create(user,current_site)
        user.password = make_password(user.password)
        user.save()
        token = AuthToken.objects.create(user)
        return Response({
            "users": UserSerializer(user, context=self.get_serializer_context()).data,
            "Please activate your accout, activation link send your email address...    "
            "token": token[1]
        })

def email_verified(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and email_verified_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return HttpResponse('Thank you for your email confirmation.')
    else:
        return HttpResponse('Activation link is invalid!')
