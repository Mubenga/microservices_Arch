import requests
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)

class JWTValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.debug("Authorization header missing or improperly formatted.")
            request.user = AnonymousUser()
            return
        
        token = auth_header.split(' ')[1]  # Extract the token
        logger.debug(f"Extracted Token: {token}")
        
        try:
            response = requests.post(
                'http://127.0.0.1:3001/validate-token',
                json={'token': token}
            )
            logger.debug(f"Token Validation Response: {response.status_code} - {response.text}")

            if response.status_code != 200:
                request.user = AnonymousUser()
                return JsonResponse({'error': 'Invalid or expired token'}, status=401)

            user_info = response.json()
            logger.debug(f"User Info: {user_info}")
            request.user = type('User', (object,), {
                'id': user_info.get('user_id'),
                'is_authenticated': True,
            })
        except requests.RequestException as e:
            logger.error(f"Error connecting to authentication service: {e}")
            request.user = AnonymousUser()
            return JsonResponse({'error': 'Authentication service unavailable'}, status=503)
