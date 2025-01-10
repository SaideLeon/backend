# visitors/serializers.py
from rest_framework import serializers
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
        # Implemente o envio do email de verificação aqui
        pass
