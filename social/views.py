# views.py
import logging
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import CommentSerializer,LikeSerializer ,ShareSerializer
from .models import Comment, Like, Share

logger = logging.getLogger(__name__)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        logger.debug("=" * 50)
        logger.debug("Creating new comment")
        logger.debug(f"Request data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            logger.debug(f"Serializer is valid. Validated data: {serializer.validated_data}")
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.debug("Comment created successfully")
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response(
                {'detail': str(e.detail[0]) if isinstance(e.detail, list) else str(e.detail)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating comment: {str(e)}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_create(self, serializer):
        logger.debug(f"Performing create with validated data: {serializer.validated_data}")
        serializer.save(author=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        chronicle_id = request.data.get('chronicle')
        
        if not chronicle_id:
            return Response(
                {'detail': 'Chronicle must be provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for existing like
        like_exists = Like.objects.filter(
            user=request.user,
            chronicle_id=chronicle_id
        ).exists()
        
        if like_exists:
            return Response(
                {'detail': 'You have already liked this chronicle'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new like
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)