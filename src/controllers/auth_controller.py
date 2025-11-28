from flask import request
from flask_restful import Resource
from src.services.auth_service import AuthService

class AuthController(Resource):
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
    
    def post(self):
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return {'message': 'Username and password required'}, 400
        
        username = data['username']
        password = data['password']
        
        token = self.auth_service.login(username, password)
        
        if token:
            return {'token': token}, 200
        else:
            return {'message': 'unauthorized'}, 401