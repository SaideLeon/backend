# urls.py
from django.urls import path
from .views import VisitorRegistrationView, VerifyEmailView

urlpatterns = [
    path('register/', VisitorRegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]