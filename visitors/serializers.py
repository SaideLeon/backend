# visitors/serializers.py
from rest_framework import serializers
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
        
        # Create user instance
        user = Visitor(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['email'],  # Using email as username
            is_active=True
        )
        
        # Set password
        user.set_password(password)
        user.save()
        
        return user
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
