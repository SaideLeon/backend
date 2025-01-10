# visitors/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

class VisitorRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VisitorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Registro realizado com sucesso! Por favor, verifique seu email.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        try:
            user = Visitor.objects.get(verification_token=token, is_verified=False)
            user.is_verified = True
            user.verification_token = None
            user.save()
            return Response({
                'message': 'Email verificado com sucesso!'
            })
        except Visitor.DoesNotExist:
            return Response({
                'error': 'Token inválido ou expirado'
            }, status=status.HTTP_400_BAD_REQUEST)

