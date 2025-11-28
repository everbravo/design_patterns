from functools import wraps
from flask import request
from src.services.auth_service import AuthService

def require_auth(auth_service: AuthService):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return {'message': 'Unauthorized: token not found'}, 401
            
            if not auth_service.validate_token(token):
                return {'message': 'Unauthorized: invalid token'}, 401
            
            return func(*args, **kwargs)
        return wrapper
    return decorator