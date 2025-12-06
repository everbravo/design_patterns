import unittest
from unittest.mock import Mock, patch
from flask import Flask
from src.controllers.cart_controller import CartController
from src.models.cart_item import CartItem

class TestCartController(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.mock_cart_service = Mock()
        self.mock_auth_service = Mock()
        self.controller = CartController(self.mock_cart_service, self.mock_auth_service)
        self.test_cart_item = CartItem(1, 1, "Test Product", 10.0, 2)
    
    def test_get_cart_success(self):
        with self.app.test_request_context('/'):
            # Setup
            expected_summary = {
                'items': [self.test_cart_item.to_dict()],
                'total_items': 2,
                'total_price': 20.0,
                'item_count': 1
            }
            self.mock_cart_service.get_cart_summary.return_value = expected_summary
            
            # Execute
            response, status_code = self.controller.get()
            
            # Verify
            self.assertEqual(status_code, 200)
            self.assertEqual(response, expected_summary)
            self.mock_cart_service.get_cart_summary.assert_called_once_with(1)
    
    @patch('src.controllers.cart_controller.reqparse.RequestParser')
    def test_post_add_item_success(self, mock_parser_class):
        with self.app.test_request_context('/', method='POST'):
            # Setup
            mock_parser = Mock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_args.return_value = {'product_id': 1, 'quantity': 2}
            
            self.mock_cart_service.add_item.return_value = self.test_cart_item
            
            # Execute
            response, status_code = self.controller.post()
        
        # Verify
        self.assertEqual(status_code, 201)
        self.assertIn('message', response)
        self.assertIn('item', response)
        self.mock_cart_service.add_item.assert_called_once_with(user_id=1, product_id=1, quantity=2)
    
    @patch('src.controllers.cart_controller.reqparse.RequestParser')
    def test_post_add_item_product_not_found(self, mock_parser_class):
        with self.app.test_request_context('/', method='POST'):
            # Setup
            mock_parser = Mock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_args.return_value = {'product_id': 999, 'quantity': 2}
            
            self.mock_cart_service.add_item.side_effect = ValueError("Product not found")
            
            # Execute
            response, status_code = self.controller.post()
        
        # Verify
        self.assertEqual(status_code, 400)
        self.assertIn('Product not found', response['message'])
    
    @patch('src.controllers.cart_controller.reqparse.RequestParser')
    def test_put_update_quantity_success(self, mock_parser_class):
        with self.app.test_request_context('/', method='PUT'):
            # Setup
            mock_parser = Mock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_args.return_value = {'quantity': 3}
            
            self.mock_cart_service.update_item_quantity.return_value = True
            
            # Execute
            response, status_code = self.controller.put(1)
        
        # Verify
        self.assertEqual(status_code, 200)
        self.assertIn('updated successfully', response['message'])
        self.mock_cart_service.update_item_quantity.assert_called_once_with(user_id=1, product_id=1, quantity=3)
    
    @patch('src.controllers.cart_controller.reqparse.RequestParser')
    def test_put_update_quantity_item_not_found(self, mock_parser_class):
        with self.app.test_request_context('/', method='PUT'):
            # Setup
            mock_parser = Mock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_args.return_value = {'quantity': 3}
            
            self.mock_cart_service.update_item_quantity.return_value = False
            
            # Execute
            response, status_code = self.controller.put(1)
        
        # Verify
        self.assertEqual(status_code, 404)
        self.assertIn('not found', response['message'])
    
    def test_put_no_product_id(self):
        with self.app.test_request_context('/', method='PUT'):
            # Execute
            response, status_code = self.controller.put(None)
        
        # Verify
        self.assertEqual(status_code, 400)
        self.assertIn('Product ID is required', response['message'])
    
    def test_delete_specific_item_success(self):
        with self.app.test_request_context('/', method='DELETE'):
            # Setup
            self.mock_cart_service.remove_item.return_value = True
            
            # Execute
            response, status_code = self.controller.delete(1)
        
        # Verify
        self.assertEqual(status_code, 200)
        self.assertIn('removed', response['message'])
        self.mock_cart_service.remove_item.assert_called_once_with(1, 1)
    
    def test_delete_specific_item_not_found(self):
        with self.app.test_request_context('/', method='DELETE'):
            # Setup
            self.mock_cart_service.remove_item.return_value = False
            
            # Execute
            response, status_code = self.controller.delete(1)
        
        # Verify
        self.assertEqual(status_code, 404)
        self.assertIn('not found', response['message'])
    
    def test_delete_clear_cart_success(self):
        with self.app.test_request_context('/', method='DELETE'):
            # Setup
            self.mock_cart_service.clear_cart.return_value = True
            
            # Execute
            response, status_code = self.controller.delete()
        
        # Verify
        self.assertEqual(status_code, 200)
        self.assertIn('cleared', response['message'])
        self.mock_cart_service.clear_cart.assert_called_once_with(1)
    
    def test_delete_clear_cart_failure(self):
        with self.app.test_request_context('/', method='DELETE'):
            # Setup
            self.mock_cart_service.clear_cart.return_value = False
            
            # Execute
            response, status_code = self.controller.delete()
        
        # Verify
        self.assertEqual(status_code, 400)
        self.assertIn('Failed to clear', response['message'])

if __name__ == '__main__':
    unittest.main()