from flask import request
from flask_restful import Resource, reqparse
from src.services.cart_service import CartService
from src.services.auth_service import AuthService
from src.decorators.auth_decorator import require_auth

class CartController(Resource):
    """Controller for cart operations"""
    
    def __init__(self, cart_service: CartService, auth_service: AuthService):
        self.cart_service = cart_service
        self.auth_service = auth_service
        self.method_decorators = [require_auth(auth_service)]
    
    def get(self, product_id=None):
        """Get cart contents or cart summary"""
        # For this demo, we'll use a fixed user_id since we don't have user management
        user_id = 1  # In a real app, this would come from the authenticated user
        
        if request.path.endswith('/summary'):
            # Get cart summary
            summary = self.cart_service.get_cart_summary(user_id)
            return summary, 200
        else:
            # Get full cart
            summary = self.cart_service.get_cart_summary(user_id)
            return summary, 200
    
    def post(self):
        """Add item to cart"""
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        
        args = parser.parse_args()
        user_id = 1  # Fixed user_id for demo
        
        try:
            cart_item = self.cart_service.add_item(
                user_id=user_id,
                product_id=args['product_id'],
                quantity=args['quantity']
            )
            
            if cart_item:
                return {
                    'message': 'Item added to cart successfully',
                    'item': cart_item.to_dict()
                }, 201
            else:
                return {'message': 'Failed to add item to cart'}, 400
                
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'Internal server error'}, 500
    
    def put(self, product_id):
        """Update item quantity in cart"""
        if not product_id:
            return {'message': 'Product ID is required'}, 400
        
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        
        args = parser.parse_args()
        user_id = 1  # Fixed user_id for demo
        
        try:
            result = self.cart_service.update_item_quantity(
                user_id=user_id,
                product_id=product_id,
                quantity=args['quantity']
            )
            
            if result:
                return {'message': 'Item quantity updated successfully'}, 200
            else:
                return {'message': 'Item not found in cart'}, 404
                
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'Internal server error'}, 500
    
    def delete(self, product_id=None):
        """Remove item from cart or clear entire cart"""
        user_id = 1  # Fixed user_id for demo
        
        try:
            if product_id:
                # Remove specific item
                result = self.cart_service.remove_item(user_id, product_id)
                if result:
                    return {'message': 'Item removed from cart successfully'}, 200
                else:
                    return {'message': 'Item not found in cart'}, 404
            else:
                # Clear entire cart
                result = self.cart_service.clear_cart(user_id)
                if result:
                    return {'message': 'Cart cleared successfully'}, 200
                else:
                    return {'message': 'Failed to clear cart'}, 400
                    
        except Exception as e:
            return {'message': 'Internal server error'}, 500