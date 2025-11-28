from flask import request
from flask_restful import Resource, reqparse
from src.services.product_service import ProductService
from src.services.auth_service import AuthService
from src.decorators.auth_decorator import require_auth

class ProductController(Resource):
    
    def __init__(self, product_service: ProductService, auth_service: AuthService):
        self.product_service = product_service
        self.auth_service = auth_service
        self.method_decorators = [require_auth(auth_service)]

    def get(self, product_id=None):
        category_filter = request.args.get('category')
        
        if category_filter:
            products = self.product_service.get_products_by_category(category_filter)
            return [p.to_dict() for p in products]
        
        if product_id is not None:
            product = self.product_service.get_product_by_id(product_id)
            if product:
                return product.to_dict()
            else:
                return {'message': 'Product not found'}, 404
        
        products = self.product_service.get_all_products()
        return [p.to_dict() for p in products]
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the product')
        parser.add_argument('category', type=str, required=True, help='Category of the product')
        parser.add_argument('price', type=float, required=True, help='Price of the product')
        
        args = parser.parse_args()
        
        try:
            product = self.product_service.create_product(
                name=args['name'],
                category=args['category'],
                price=args['price']
            )
            return {'message': 'Product added', 'product': product.to_dict()}, 201
        except ValueError as e:
            return {'message': str(e)}, 400