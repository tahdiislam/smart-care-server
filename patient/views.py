from django.shortcuts import  redirect
from .serializers import PatientSerializer, RegistrationSerializer, LoginSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Patient
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

#for sending mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print('token', token)
            print('uid', uid)
            full_name = f'{user.first_name} {user.last_name}'
            confirm_url = f'http://127.0.0.1:8000/patient/activate/{uid}/{token}'
            email_subject = 'Confirm your account'
            email_body = render_to_string('patient/confirm_email.html',{'confirm_url': confirm_url, 'full_name': full_name})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response('Check your email to confirm your account') 
        
        return Response(serializer.errors)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('register')
    else:
        return redirect('register')

class UserLoginApiView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.id})

        return Response({'error': 'Invalid credentials'})