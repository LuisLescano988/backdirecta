from jose import jwt
from jose.exceptions import JWTError
from django.http import JsonResponse
import requests
from django.conf import settings

class Auth0TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                return JsonResponse({'error': 'No authorization token'}, status=401)
            
            try:
                # Extraer token
                token = auth_header.split(' ')[1]
                
                # Obtener JWKS (JSON Web Key Set)
                jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
                jwks_response = requests.get(jwks_url)
                jwks = jwks_response.json()
                
                # Decodificar y validar token
                unverified_header = jwt.get_unverified_header(token)
                rsa_key = {}
                for key in jwks['keys']:
                    if key['kid'] == unverified_header['kid']:
                        rsa_key = {
                            'kty': key['kty'],
                            'kid': key['kid'],
                            'use': key['use'],
                            'n': key['n'],
                            'e': key['e']
                        }
                
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=settings.ALGORITHMS,
                    audience=settings.AUTH0_AUDIENCE,
                    issuer=f'https://{settings.AUTH0_DOMAIN}/'
                )
                
                # Puedes agregar el usuario al request si lo necesitas
                request.user_info = payload
                
            except (JWTError, KeyError, IndexError):
                return JsonResponse({'error': 'Invalid token'}, status=401)
        
        return self.get_response(request)