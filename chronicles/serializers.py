from rest_framework import serializers
from .models import Chronicle, FeaturedChronicle
from django.utils.formats import date_format
from django.utils.translation import gettext as _
import locale

# Configurar locale para português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        pass

class ChronicleSerializer(serializers.ModelSerializer):
    date_formatted = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Chronicle
        fields = [
            'id', 
            'date', 
            'date_formatted', 
            'title', 
            'content', 
            'pdf_file',
            'pdf_url',
            'author',
            'author_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']
        
    def get_date_formatted(self, obj):
        """Retorna a data formatada em português"""
        try:
            return obj.date.strftime("%d de %B de %Y").lower()
        except:
            return date_format(obj.date, format="d \d\e F \d\e Y", use_l10n=True)

    def get_author_name(self, obj):
        """Retorna o nome do autor"""
        return obj.author.get_full_name() or obj.author.username
    
    def get_pdf_url(self, obj):
        """Retorna a URL completa do PDF se existir"""
        if obj.pdf_file:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.pdf_file.url)
        return None

    def validate_author(self, value):
        """Valida se o autor é um superusuário"""
        if not value.is_superuser:
            raise serializers.ValidationError(
                _("Apenas superusuários podem criar ou editar crônicas.")
            )
        return value

class FeaturedChronicleSerializer(serializers.ModelSerializer):
    date_formatted = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FeaturedChronicle
        fields = [
            'id', 
            'date', 
            'date_formatted', 
            'title', 
            'content', 
            'pdf_file',
            'pdf_url',
            'user',
            'user_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
        
    def get_date_formatted(self, obj):
        """Retorna a data formatada em português"""
        try:
            return obj.date.strftime("%d de %B de %Y").lower()
        except:
            return date_format(obj.date, format="d \d\e F \d\e Y", use_l10n=True)

    def get_user_name(self, obj):
        """Retorna o nome do usuário"""
        return obj.user.get_full_name() or obj.user.username
    
    def get_pdf_url(self, obj):
        """Retorna a URL completa do PDF"""
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None

    def validate_user(self, value):
        """Valida se o usuário é um superusuário"""
        if not value.is_superuser:
            raise serializers.ValidationError(
                _("Apenas superusuários podem criar ou editar crônicas principais.")
            )
        return value

    def create(self, validated_data):
        """
        Sobrescreve o método create para garantir que cada usuário
        tenha apenas uma crônica principal
        """
        user = self.context['request'].user
        # Remove qualquer crônica principal existente do usuário
        FeaturedChronicle.objects.filter(user=user).delete()
        # Cria a nova crônica principal
        return super().create(validated_data)