# urls.py
from django.urls import path
from .views import VisitorRegistrationView, LoginView

urlpatterns = [
    path('register/', VisitorRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]