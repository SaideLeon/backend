# visitors/backends.py
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import Visitor

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if we're using email or username
            email = username
            if not email:
                email = kwargs.get('email')
            
            if email is None:
                return None
                
            user = Visitor.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except Visitor.DoesNotExist:
            return None