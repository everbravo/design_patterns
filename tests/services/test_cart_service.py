import unittest
from unittest.mock import Mock, MagicMock
from src.services.cart_service import CartService
from src.models.cart_item import CartItem
from src.models.product import Product

class TestCartService(unittest.TestCase):
    
    def setUp(self):
        self.mock_cart_repository = Mock()
        self.mock_product_service = Mock()
        self.mock_pricing_strategy = Mock()
        
        self.cart_service = CartService(
            self.mock_cart_repository,
            self.mock_product_service,
            self.mock_pricing_strategy
        )
        
        self.test_product = Product(1, "Test Product", "electronics", 10.0)
        self.test_cart_item = CartItem(1, 1, "Test Product", 10.0, 2)
    
    def test_add_item_success(self):
        # Setup mocks
        self.mock_product_service.get_product_by_id.return_value = self.test_product
        self.mock_cart_repository.add_item.return_value = self.test_cart_item
        
        # Execute
        result = self.cart_service.add_item(1, 1, 2)
        
        # Verify
        self.assertIsNotNone(result)
        self.mock_product_service.get_product_by_id.assert_called_once_with(1)
        self.mock_cart_repository.add_item.assert_called_once()
    
    def test_add_item_product_not_found(self):
        # Setup mocks
        self.mock_product_service.get_product_by_id.return_value = None
        
        # Execute & Verify
        with self.assertRaises(ValueError):
            self.cart_service.add_item(1, 999, 2)
    
    def test_add_item_invalid_quantity(self):
        # Execute & Verify
        with self.assertRaises(ValueError):
            self.cart_service.add_item(1, 1, 0)
    
    def test_remove_item_success(self):
        # Setup mocks
        self.mock_cart_repository.remove_item.return_value = True
        
        # Execute
        result = self.cart_service.remove_item(1, 1)
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_repository.remove_item.assert_called_once_with(1, 1)
    
    def test_update_item_quantity_success(self):
        # Setup mocks
        self.mock_cart_repository.get_item.return_value = self.test_cart_item
        self.mock_cart_repository.update_item_quantity.return_value = True
        
        # Execute
        result = self.cart_service.update_item_quantity(1, 1, 3)
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_repository.update_item_quantity.assert_called_once_with(1, 1, 3)
    
    def test_update_item_quantity_zero_removes_item(self):
        # Setup mocks
        self.mock_cart_repository.remove_item.return_value = True
        
        # Execute
        result = self.cart_service.update_item_quantity(1, 1, 0)
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_repository.remove_item.assert_called_once_with(1, 1)
    
    def test_get_cart_items(self):
        # Setup mocks
        expected_items = [self.test_cart_item]
        self.mock_cart_repository.get_cart_by_user_id.return_value = expected_items
        
        # Execute
        result = self.cart_service.get_cart_items(1)
        
        # Verify
        self.assertEqual(result, expected_items)
        self.mock_cart_repository.get_cart_by_user_id.assert_called_once_with(1)
    
    def test_clear_cart_success(self):
        # Setup mocks
        self.mock_cart_repository.clear_cart.return_value = True
        
        # Execute
        result = self.cart_service.clear_cart(1)
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_repository.clear_cart.assert_called_once_with(1)
    
    def test_get_cart_summary(self):
        # Setup mocks
        items = [self.test_cart_item]
        self.mock_cart_repository.get_cart_by_user_id.return_value = items
        self.mock_pricing_strategy.calculate_cart_total.return_value = 20.0
        
        # Execute
        result = self.cart_service.get_cart_summary(1)
        
        # Verify
        expected = {
            'items': [self.test_cart_item.to_dict()],
            'total_items': 2,
            'total_price': 20.0,
            'item_count': 1
        }
        self.assertEqual(result, expected)
    
    def test_observer_notifications(self):
        # Setup observer mock
        mock_observer = Mock()
        self.cart_service.add_observer(mock_observer)
        
        # Setup mocks for add_item
        self.mock_product_service.get_product_by_id.return_value = self.test_product
        self.mock_cart_repository.add_item.return_value = self.test_cart_item
        
        # Execute
        self.cart_service.add_item(1, 1, 2)
        
        # Verify observer was notified
        mock_observer.on_item_added.assert_called_once()

if __name__ == '__main__':
    unittest.main()