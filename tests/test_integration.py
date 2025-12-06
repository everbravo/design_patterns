import unittest
import tempfile
import json
import os
from src.container import Container
from src.config.config import Config

class TestIntegration(unittest.TestCase):
    """Integration tests for the entire cart module"""
    
    def setUp(self):
        # Create temporary database file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file_path = self.temp_file.name
        
        # Initialize with test data
        initial_data = {
            "products": [
                {"id": 1, "name": "Test Product", "category": "electronics", "price": 10.0},
                {"id": 2, "name": "Another Product", "category": "books", "price": 15.0}
            ],
            "categories": [
                {"id": 1, "name": "electronics"},
                {"id": 2, "name": "books"}
            ],
            "favorites": [],
            "carts": []
        }
        json.dump(initial_data, self.temp_file)
        self.temp_file.close()
        
        # Override config for testing
        Config.DATABASE_FILE = self.temp_file_path
        
        # Create container with test database
        self.container = Container()
        self.cart_service = self.container.get('cart_service')
        self.product_service = self.container.get('product_service')
    
    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)
    
    def test_full_cart_workflow(self):
        """Test complete cart workflow: add, update, remove, clear"""
        user_id = 1
        
        # 1. Add item to cart
        cart_item = self.cart_service.add_item(user_id, 1, 2)
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 2)
        
        # 2. Verify cart contents
        cart_items = self.cart_service.get_cart_items(user_id)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0].product_id, 1)
        
        # 3. Add another item
        self.cart_service.add_item(user_id, 2, 1)
        cart_items = self.cart_service.get_cart_items(user_id)
        self.assertEqual(len(cart_items), 2)
        
        # 4. Update quantity
        result = self.cart_service.update_item_quantity(user_id, 1, 5)
        self.assertTrue(result)
        
        # 5. Verify update
        updated_item = self.cart_service.get_cart_item(user_id, 1)
        self.assertEqual(updated_item.quantity, 5)
        
        # 6. Get cart summary
        summary = self.cart_service.get_cart_summary(user_id)
        self.assertEqual(summary['total_items'], 6)  # 5 + 1
        self.assertEqual(summary['item_count'], 2)
        self.assertEqual(summary['total_price'], 65.0)  # (10*5) + (15*1)
        
        # 7. Remove one item
        result = self.cart_service.remove_item(user_id, 2)
        self.assertTrue(result)
        
        # 8. Verify removal
        cart_items = self.cart_service.get_cart_items(user_id)
        self.assertEqual(len(cart_items), 1)
        
        # 9. Clear cart
        result = self.cart_service.clear_cart(user_id)
        self.assertTrue(result)
        
        # 10. Verify cart is empty
        cart_items = self.cart_service.get_cart_items(user_id)
        self.assertEqual(len(cart_items), 0)
    
    def test_cart_with_invalid_product(self):
        """Test adding non-existent product to cart"""
        user_id = 1
        
        with self.assertRaises(ValueError):
            self.cart_service.add_item(user_id, 999, 1)
    
    def test_multiple_users_carts(self):
        """Test that different users have separate carts"""
        user1_id = 1
        user2_id = 2
        
        # Add items to different user carts
        self.cart_service.add_item(user1_id, 1, 2)
        self.cart_service.add_item(user2_id, 2, 3)
        
        # Verify separation
        user1_items = self.cart_service.get_cart_items(user1_id)
        user2_items = self.cart_service.get_cart_items(user2_id)
        
        self.assertEqual(len(user1_items), 1)
        self.assertEqual(len(user2_items), 1)
        self.assertEqual(user1_items[0].product_id, 1)
        self.assertEqual(user2_items[0].product_id, 2)
    
    def test_cart_persistence(self):
        """Test that cart data persists across service instances"""
        user_id = 1
        
        # Add item with first service instance
        self.cart_service.add_item(user_id, 1, 2)
        
        # Create new container (simulating app restart)
        new_container = Container()
        new_cart_service = new_container.get('cart_service')
        
        # Verify data persisted
        cart_items = new_cart_service.get_cart_items(user_id)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0].quantity, 2)
    
    def test_pricing_strategy_integration(self):
        """Test that pricing strategies work with cart service"""
        user_id = 1
        
        # Add items to cart
        self.cart_service.add_item(user_id, 1, 2)  # 10.0 * 2 = 20.0
        self.cart_service.add_item(user_id, 2, 1)  # 15.0 * 1 = 15.0
        
        # Get total using pricing strategy
        total = self.cart_service.get_cart_total(user_id)
        self.assertEqual(total, 35.0)
        
        # Verify summary calculation
        summary = self.cart_service.get_cart_summary(user_id)
        self.assertEqual(summary['total_price'], 35.0)

if __name__ == '__main__':
    unittest.main()