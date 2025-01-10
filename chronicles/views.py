from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import Chronicle, FeaturedChronicle
from .serializers import ChronicleSerializer, FeaturedChronicleSerializer

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada que permite apenas superusuários
    criar, editar ou excluir objetos.
    """
    def has_permission(self, request, view):
        # Permite visualização para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Requer superusuário para outras operações
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Permite visualização para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Requer superusuário para outras operações
        return request.user and request.user.is_superuser

class ChronicleViewSet(viewsets.ModelViewSet):
    queryset = Chronicle.objects.all()
    serializer_class = ChronicleSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        """
        Salva o autor automaticamente como o usuário atual
        """
        if not self.request.user.is_superuser:
            raise ValidationError(_("Apenas superusuários podem criar crônicas."))
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        """
        Customiza a queryset com ordenação e possíveis filtros
        """
        queryset = Chronicle.objects.all().order_by('-date', '-created_at')
        
        # Exemplo de filtros opcionais por query params
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(date=date)
            
        author = self.request.query_params.get('author', None)
        if author is not None and self.request.user.is_superuser:
            queryset = queryset.filter(author__username=author)
            
        return queryset

class FeaturedChronicleViewSet(viewsets.ModelViewSet):
    queryset = FeaturedChronicle.objects.all()
    serializer_class = FeaturedChronicleSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        """
        Salva o usuário automaticamente e garante que só exista
        uma crônica principal por usuário
        """
        if not self.request.user.is_superuser:
            raise ValidationError(_("Apenas superusuários podem criar crônicas principais."))
            
        # Remove crônica principal existente do usuário
        FeaturedChronicle.objects.filter(user=self.request.user).delete()
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        """
        Customiza a queryset com ordenação e possíveis filtros
        """
        queryset = FeaturedChronicle.objects.all().order_by('-date', '-created_at')
        
        # Exemplo de filtros opcionais por query params
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(date=date)
            
        user = self.request.query_params.get('user', None)
        if user is not None and self.request.user.is_superuser:
            queryset = queryset.filter(user__username=user)
            
        return queryset

