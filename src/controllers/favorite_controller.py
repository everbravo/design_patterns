from flask import request
from flask_restful import Resource, reqparse
from src.services.favorite_service import FavoriteService
from src.services.auth_service import AuthService
from src.decorators.auth_decorator import require_auth

class FavoriteController(Resource):
    
    def __init__(self, favorite_service: FavoriteService, auth_service: AuthService):
        self.favorite_service = favorite_service
        self.auth_service = auth_service
        self.method_decorators = [require_auth(auth_service)]
    
    def get(self):
        favorites = self.favorite_service.get_all_favorites()
        return [f.to_dict() for f in favorites], 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        
        args = parser.parse_args()
        
        favorite = self.favorite_service.add_favorite(
            user_id=args['user_id'],
            product_id=args['product_id']
        )
        return {'message': 'Product added to favorites', 'favorite': favorite.to_dict()}, 201
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        
        args = parser.parse_args()
        
        if self.favorite_service.remove_favorite(args['user_id'], args['product_id']):
            return {'message': 'Product removed from favorites'}, 200
        else:
            return {'message': 'Favorite not found'}, 404