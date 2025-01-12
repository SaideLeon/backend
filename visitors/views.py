# visitors/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .serializers import VisitorRegistrationSerializer  # Add this import
from .models import Visitor

class VisitorRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VisitorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Registro realizado com sucesso! Por favor, verifique seu email.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        try:
            user = Visitor.objects.get(verification_token=token, is_verified=False)
            user.is_verified = True
            user.verification_token = None
            user.save()
            return Response({
                'message': 'Email verificado com sucesso!'
            })
        except Visitor.DoesNotExist:
            return Response({
                'error': 'Token inválido ou expirado'
            }, status=status.HTTP_400_BAD_REQUEST)

# visitors/serializers.py
from rest_framework import serializers
from django.utils.crypto import get_random_string  # Add this import
from .models import Visitor

class VisitorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Visitor
        fields = ['email', 'name', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        validated_data['username'] = validated_data['email']  # Usando email como username
        
        user = Visitor(**validated_data)
        user.set_password(password)
        user.verification_token = get_random_string(64)
        user.save()
        
        self.send_verification_email(user)
        return user
    
    def send_verification_email(self, user):
        # Template para o email
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={user.verification_token}"
        subject = 'Confirme seu email - Crônicas de Moçambique'
        message = f"""
        Olá {user.name},

        Obrigado por se registrar no Crônicas de Moçambique! 
        Para confirmar seu email, clique no link abaixo:

        {verification_url}

        Se você não se registrou no nosso site, ignore este email.

        Atenciosamente,
        Equipe Crônicas de Moçambique
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't prevent user creation
            print(f"Error sending verification email: {str(e)}")