from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
import jwt
from django.conf import settings
from django.http import JsonResponse

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        
        try:
            id_info = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID,
            )

            email = id_info['email']
            name = id_info['name']
            
            user, created = User.objects.get_or_create(
                username=email,
                defaults={'first_name': name}
            )
            
            access_token = self.generate_access_token(user)
            refresh_token = self.generate_refresh_token(user)
            
            response = JsonResponse({
                'user': {
                    'name': name,
                    'email': email,
                    'picture': id_info.get('picture', '')
                }
            })
            
            response.set_cookie(
                'refresh_token', 
                refresh_token, 
                httponly=True,
                secure=True,  
                samesite='Strict'
            )
            
            response.data = {
                'token': access_token
            }
            
            return response
        
        except ValueError:
            return Response(
                {'error': 'Invalid token'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    def generate_access_token(self, user):
        return jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + settings.JWT_SETTINGS['ACCESS_TOKEN_LIFETIME']
        }, settings.JWT_SETTINGS['SECRET_KEY'], algorithm='HS256')
    
    def generate_refresh_token(self, user):
        return jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + settings.JWT_SETTINGS['REFRESH_TOKEN_LIFETIME']
        }, settings.JWT_SETTINGS['SECRET_KEY'], algorithm='HS256')

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        try:
            
            payload = jwt.decode(
                refresh_token, 
                settings.JWT_SETTINGS['SECRET_KEY'], 
                algorithms=['HS256']
            )
            
            
            user = User.objects.get(id=payload['user_id'])
            
            
            new_access_token = self.generate_access_token(user)
            
            return Response({
                'token': new_access_token
            })
        
        except jwt.ExpiredSignatureError:
            return Response(
                {'error': 'Refresh token expirado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_401_UNAUTHORIZED
            )