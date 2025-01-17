# social/models.py
from django.db import models
from django.conf import settings
from chronicles.models import Chronicle
from django.urls import reverse

class Comment(models.Model):
    chronicle = models.ForeignKey(
        Chronicle, 
        on_delete=models.CASCADE, null=True,blank=True,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return f"Comentário por {self.author.name} em {self.chronicle.title}"


class Like(models.Model):
    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'chronicle')]
        verbose_name = "Curtida"
        verbose_name_plural = "Curtidas"

    def __str__(self):
        return f"Curtida por {self.user.name} em {self.chronicle.title}"

class Share(models.Model):
    PLATFORMS = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
    )
    
    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Compartilhamento"
        verbose_name_plural = "Compartilhamentos"

    def __str__(self):
        return f"Compartilhamento {self.platform} por {self.user.name}"