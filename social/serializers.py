# serializers.py
import logging
from rest_framework import serializers
from .models import Comment, Like, Share
from django.urls import reverse
from chronicles.models import Chronicle

logger = logging.getLogger(__name__)

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    chronicle = serializers.PrimaryKeyRelatedField(
        queryset=Chronicle.objects.all(), 
        required=True
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'author_name', 'created_at', 
                 'updated_at', 'is_approved', 'chronicle']
        read_only_fields = ['author', 'is_approved', 'created_at', 'updated_at']
        
    def get_author_name(self, obj):
        return obj.author.name if hasattr(obj, 'author') else self.context['request'].user.name

    def validate(self, data):
        logger.debug(f"Validating comment data: {data}")
        
        if 'chronicle' not in data:
            raise serializers.ValidationError("Chronicle field is required")
            
        return data

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'chronicle', 'created_at']
        read_only_fields = ['user', 'created_at']

class ShareSerializer(serializers.ModelSerializer):
    share_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Share
        fields = ['id', 'user', 'platform', 'chronicle', 'created_at', 'share_url']
        read_only_fields = ['user', 'created_at', 'share_url']
        
    def get_share_url(self, obj):
        if isinstance(obj, dict):
            chronicle_id = obj.get('chronicle')
        else:
            chronicle_id = obj.chronicle.id
            
        base_url = self.context['request'].build_absolute_uri('/')
        chronicle_url = reverse('chronicle-detail', args=[chronicle_id])
        full_url = base_url.rstrip('/') + chronicle_url
        
        platform = obj.get('platform') if isinstance(obj, dict) else obj.platform
        
        share_urls = {
            'facebook': f"https://www.facebook.com/sharer/sharer.php?u={full_url}",
            'twitter': f"https://twitter.com/intent/tweet?url={full_url}",
            'whatsapp': f"https://api.whatsapp.com/send?text={full_url}",
            'telegram': f"https://t.me/share/url?url={full_url}"
        }
        
        return share_urls.get(platform, full_url)