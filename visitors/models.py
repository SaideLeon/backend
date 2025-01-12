# visitors/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class Visitor(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Customizing related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='visitor_groups',  # Custom related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='visitor_permissions',  # Custom related_name
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        
    