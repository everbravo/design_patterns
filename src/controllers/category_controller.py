from flask import request
from flask_restful import Resource, reqparse
from src.services.category_service import CategoryService
from src.services.auth_service import AuthService
from src.decorators.auth_decorator import require_auth

class CategoryController(Resource):
    
    def __init__(self, category_service: CategoryService, auth_service: AuthService):
        self.category_service = category_service
        self.auth_service = auth_service
        self.method_decorators = [require_auth(auth_service)]
    
    def get(self, category_id=None):
        if category_id is not None:
            category = self.category_service.get_category_by_id(category_id)
            if category:
                return category.to_dict()
            else:
                return {'message': 'Category not found'}, 404
        
        categories = self.category_service.get_all_categories()
        return [c.to_dict() for c in categories]
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the category')
        
        args = parser.parse_args()
        
        try:
            category = self.category_service.create_category(name=args['name'])
            return {'message': 'Category added successfully'}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the category')
        
        args = parser.parse_args()
        
        if self.category_service.delete_category_by_name(args['name']):
            return {'message': 'Category removed successfully'}, 200
        else:
            return {'message': 'Category not found'}, 404