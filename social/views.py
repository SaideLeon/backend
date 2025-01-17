import logging
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import CommentSerializer, LikeSerializer, ShareSerializer
from .models import Comment, Like, Share

logger = logging.getLogger(__name__)

class BaseChronicleViewSet(viewsets.ModelViewSet):
    """
    Classe base para views relacionadas a crônicas. 
    Inclui métodos utilitários para reutilização.
    """
    def get_queryset(self):
        queryset = self.queryset
        chronicle_id = self.request.query_params.get('chronicle')
        user_id = self.request.query_params.get('user')
        
        if chronicle_id:
            queryset = queryset.filter(chronicle_id=chronicle_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset

class CommentViewSet(BaseChronicleViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        logger.info("Iniciando criação de comentário...")
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info("Comentário criado com sucesso.")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.warning(f"Erro de validação: {e}")
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro ao criar comentário: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        logger.debug(f"Salvando comentário: {serializer.validated_data}")
        serializer.save(author=self.request.user)

class LikeViewSet(BaseChronicleViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        chronicle_id = request.data.get('chronicle')
        if not chronicle_id:
            return Response({'detail': 'ID da crônica é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Like.objects.filter(user=request.user, chronicle_id=chronicle_id).exists():
            return Response({'detail': 'Você já curtiu esta crônica'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info("Curtida adicionada com sucesso.")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.warning(f"Erro de validação ao curtir: {e}")
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro ao curtir crônica: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        logger.debug("Adicionando curtida...")
        serializer.save(user=self.request.user)

class ShareViewSet(BaseChronicleViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        logger.info("Iniciando compartilhamento de crônica...")
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info("Compartilhamento realizado com sucesso.")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.warning(f"Erro de validação ao compartilhar: {e}")
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro ao compartilhar crônica: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        logger.debug("Salvando compartilhamento...")
        serializer.save(user=self.request.user)
