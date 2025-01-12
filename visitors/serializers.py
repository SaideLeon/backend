# visitors/serializers.py
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import Visitor

class VisitorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Visitor
        fields = ['email', 'name', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True}
        }

    def validate_email(self, value):
        if Visitor.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({
                "password_confirm": "As senhas não coincidem"
            })
        return data

    def create(self, validated_data):
        # Remove password_confirm from the data
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        
        # Create user instance but don't save yet
        user = Visitor(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['email'],  # Using email as username
            is_active=True,  # User can login but needs email verification
            is_verified=False  # Email not verified yet
        )
        
        # Set password and verification token
        user.set_password(password)
        user.verification_token = get_random_string(64)
        user.save()
        
        # Send verification email
        self.send_verification_email(user)
        
        return user

    def send_verification_email(self, user):
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