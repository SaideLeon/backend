# visitors/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import VisitorRegistrationSerializer, LoginSerializer
from .models import Visitor
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db import transaction  # Added this import
import logging

logger = logging.getLogger(__name__)

class VisitorRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            logger.info("Iniciando processo de registro de novo visitante")
            serializer = VisitorRegistrationSerializer(data=request.data)
            
            if serializer.is_valid():
                logger.info("Dados de registro validados com sucesso")
                user = serializer.save()
                logger.info(f"Novo visitante registrado com sucesso: {user.email}")
                
                return Response({
                    'message': 'Registro realizado com sucesso!'
                }, status=status.HTTP_201_CREATED)
            
            logger.error(f"Erro na validação dos dados de registro: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro inesperado durante o registro: {str(e)}", exc_info=True)
            return Response({
                'error': 'Erro interno do servidor durante o registro'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            logger.info("Iniciando processo de login")
            serializer = LoginSerializer(data=request.data)
            
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                
                logger.info(f"Tentativa de login para o email: {email}")
                
                try:
                    # Primeiro, verificamos se o usuário existe
                    try:
                        user = Visitor.objects.get(email=email)
                    except Visitor.DoesNotExist:
                        logger.warning(f"Usuário não encontrado: {email}")
                        return Response({
                            'error': 'Usuário não encontrado'
                        }, status=status.HTTP_401_UNAUTHORIZED)

                    # Depois autenticamos
                    if not user.check_password(password):
                        logger.warning(f"Senha incorreta para usuário: {email}")
                        return Response({
                            'error': 'Senha incorreta'
                        }, status=status.HTTP_401_UNAUTHORIZED)

                    # Se chegou aqui, o usuário está autenticado
                    logger.info(f"Usuário autenticado com sucesso: {email}")

                    # Gerenciamos o token em uma transação
                    with transaction.atomic():
                        # Primeiro removemos qualquer token existente
                        Token.objects.filter(user=user).delete()
                        
                        # Criamos um novo token
                        token = Token.objects.create(user=user)
                        
                        logger.info(f"Token criado com sucesso para: {email}")
                        
                        return Response({
                            'token': token.key,
                            'user': {
                                'id': user.id,
                                'email': user.email,
                                'name': user.name
                            }
                        })

                except Exception as e:
                    logger.error(f"Erro durante autenticação: {str(e)}", exc_info=True)
                    return Response({
                        'error': 'Erro durante autenticação'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            logger.error(f"Dados de login inválidos: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
            return Response({
                'error': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)